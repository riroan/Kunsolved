from bs4 import BeautifulSoup
from database import SessionLocal, engine
from tqdm import tqdm
from contextlib import contextmanager

import requests
import time
import json
import datetime
import crud
import schemas
import models

import log


def add_day(sourceDate, count):
    targetDate = sourceDate + datetime.timedelta(days=count)
    return targetDate


def get_week_date(sourceDate):
    temporaryDate = datetime.datetime(
        sourceDate.year, sourceDate.month, sourceDate.day)
    weekDayCount = temporaryDate.weekday()
    startDate = add_day(temporaryDate, -weekDayCount)
    endDate = add_day(startDate, 7)
    return str(startDate), str(endDate)


class Utility:
    def __init__(self, debug_mode=False):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        self.debug_mode = debug_mode

    @contextmanager
    def get_session(self):
        self.session = SessionLocal()
        try:
            yield self.session
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    # 특정 유저가 해결한 문제들 반환
    def get_user_info(self, user):
        url = f"https://acmicpc.net/user/{user}"
        time.sleep(10)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select(
                'div.panel-body > div.problem-list')[0].text.strip().split(" ")
            return [int(element) for element in elements]
        else:
            return []

    # 특정 학교 구성원의 아이디 반환
    def get_school_info(self, number, page=1):
        url = f"https://www.acmicpc.net/school/ranklist/{number}/{page}"
        response = requests.get(url, headers=self.headers)
        time.sleep(10)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            users = soup.select('#ranklist tr > td:nth-child(2) a')
            return [user.text for user in users]
        else:
            return []

    # 특정 학교 구성원이 최근에 해결한 문제 반환
    def get_recent_solved(self, number=194):
        log.info("get_recent_solved")
        url = f"https://www.acmicpc.net/status?school_id={number}"
        response = requests.get(url, headers=self.headers)
        time.sleep(10)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            users = soup.select(
                '#status-table > tbody > tr > td:nth-child(2) > a')

            users = [user.text for user in users]

            problems = soup.select(
                '#status-table > tbody > tr > td:nth-child(3) > a')
            problems = [problem.text for problem in problems]
            status = soup.select(
                '#status-table > tbody > tr > td:nth-child(4) > span')

            status = [str(st) for st in status if st.text != '\xa0']

            ret_user, ret_problem = [], []
            for user, problem, st in zip(users, problems, status):
                if "result-ac" in st:
                    ret_user.append(user)
                    ret_problem.append(problem)
            return ret_user, ret_problem
        else:
            return [], []

    def add_recent_solved(self, number=194):
        log.info("add_recent_solved")
        users, problems = self.get_recent_solved(number)
        with self.get_session() as session:
            for user, problem_id in zip(users, problems):
                data = crud.read_solve(session, problem_id, user)
                if data is None:
                    crud.create_solve(session, schemas.SolveCreate(
                        name=user, id=problem_id))

    # 존재하는 모든 문제 아이디, 제목을 db에 추가 이미 있으면 태그, 티어 업데이트
    def get_problem_info(self):
        log.info("get_problem_info")
        ix = 1
        with self.get_session() as session:
            while True:
                url = f"https://solved.ac/api/v3/search/problem?query=solvable:true&page={ix}"
                time.sleep(3)
                response = requests.get(url)
                try:
                    items = json.loads(response.text)
                except Exception:
                    print(response.text)
                    continue
                problems = items['items']
                if len(problems) == 0:
                    break
                for problem in problems:
                    number = problem['problemId']
                    title = problem['titleKo']
                    title = title.replace("\\", "\\\\").replace(
                        "'", "\\'").replace('"', '\\"').replace("%", "%%")
                    level = problem['level']
                    tags = problem['tags']
                    num_solved = problem["acceptedUserCount"]
                    try:
                        crud.create_problem(session, schemas.ProblemCreate(
                            id=number, title=title, tier=level, num_solved=num_solved))
                        for tag in tags:
                            for displayNames in tag['displayNames']:
                                if displayNames['language'] == 'ko':
                                    t = displayNames['name']
                            crud.create_tag(
                                session, schemas.TagCreate(id=number, name=t))
                    except Exception:
                        if self.debug_mode:
                            print(f">> Problem {number} is already existed")
                        session.rollback()
                        crud.update_problem_tier(session, number, level)
                        existed = crud.read_tag(session, number)
                        e = {i.name: True for i in existed}
                        need = []
                        for tag in tags:
                            for displayNames in tag['displayNames']:
                                if displayNames['language'] == 'ko':
                                    t = displayNames['name']
                            if t not in e:
                                need.append(t)
                        if need:
                            for v in need:
                                crud.create_tag(
                                    session, schemas.TagCreate(id=number, name=v))
                            if self.debug_mode:
                                print(f">> Problem {number}'s tag is updated")
                        crud.update_problem_num_solved(
                            session, number, num_solved)
                ix += 1

    # 특정 학교에 존재하는 모든 유저 아이디 반환
    def get_all_user(self, number):
        ix = 1
        users = []
        while True:
            info = self.get_school_info(number, ix)
            if len(info) == 0:
                break
            users.extend(info)
            ix += 1
        return users

    # 특정 학교에 존재하는 모든 유저 아이디 db에 추가
    def update_school_user(self, number=194):
        log.info("update_school_user")
        users = self.get_all_user(number)
        with self.get_session() as session:
            for user in users:
                try:
                    crud.create_user(session, schemas.UserCreate(name=user))
                except Exception:
                    session.rollback()
                    if self.debug_mode:
                        print(f">> Warning : User {user} is already existed")

    # 특정 학교에 존재하는 모든 유저의 해결한 문제 업데이트
    def update_all_user_solved(self):
        log.info("update_all_user_solved")
        with self.get_session() as session:
            users = crud.read_all_user(session)
            users = [user.name for user in users]
            for user in tqdm(users):
                solved = self.get_user_info(user)
                for solve in solved:
                    data = crud.read_solve(session, solve, user)
                    if data:
                        if self.debug_mode:
                            print(
                                f">> Warning : Problem {solve} solved by {user} is already existed")
                        continue
                    crud.create_solve(
                        session, schemas.SolveCreateWithTime(name=user, id=solve, solved_at=datetime.datetime(1900, 1, 1, 0, 0, 0)))
                    crud.update_problem_is_solved(session, solve)
                    if self.debug_mode:
                        print(
                            f">> Log : Problem {solve} solved by {user} is appended")

    # 특정 학교 구성원이 해결한 모든 문제 반환
    def get_problem_solved_by_tag(self, tag, session):
        data = crud.read_problem_solved_by_tag(session, tag)
        return data

    # 특정 학교 구성원이 해결한 모든 문제를 난이도별 개수로 반환
    def get_problem_solved_by_level(self, session, verbose=0):
        cnt = [0]
        data = crud.read_all_problem_solved(session)
        if verbose == 0:  # 브론즈, 실버, 골드...
            NUM_TIER = 7
            cnt = [0] * NUM_TIER
            for d in data:
                cnt[(d.tier+4)//5] += 1
        elif verbose == 1:  # 브론즈5, 브론즈4, 브론즈3, ...
            NUM_TIER = 31
            cnt = [0] * NUM_TIER
            for d in data:
                cnt[d['tier']] += d['cnt']
        return cnt

    def get_count_all_solved_by_tag(self):
        ret = dict()
        with self.get_session() as session:
            data = crud.read_count_solved_by_tag(session, "수학")  # 수정 필요
            for d in data:
                ret[d['name']] = d['cnt']
        return ret

    def get_count_solved_by_tag(self, tag):
        try:
            return self.get_count_all_solved_by_tag()[tag]
        except KeyError:
            return 0

    def get_all_exp(self, session):
        pass
        # query = "SELECT * FROM experience;"
        # data = self.db.executeAll(query)
        # NUM_TIER = 31
        # ret = [0]*NUM_TIER
        # for d in data:
        #     ret[d['tier']] = d['exp']
        # return ret

    def get_status_by_level(self, session):
        data = {}
        all_count = crud.read_all_problem_count_by_tier(session)
        solved_count = crud.read_problem_solved_count_by_tier(session)
        all_count_dict = {}
        solved_count_dict = {}

        for cnt, tier in all_count:
            all_count_dict[tier] = cnt
        for cnt, tier in solved_count:
            solved_count_dict[tier] = cnt

        for cnt, tier in all_count:
            data[tier] = {"all_cnt": all_count_dict[tier], "solved_cnt": 0}
        for cnt, tier in solved_count:
            data[tier]["solved_cnt"] = cnt
        return data

    def get_status_by_tag(self, session):
        data = {}
        all_count = crud.read_all_problem_count_by_tag(session)
        solved_count = crud.read_problem_solved_count_by_tag(session)
        all_count_dict = {}
        solved_count_dict = {}

        for cnt, tag in all_count:
            all_count_dict[tag] = cnt
        for cnt, tag in solved_count:
            solved_count_dict[tag] = cnt

        for cnt, tag in all_count:
            data[tag] = {"all_cnt": all_count_dict[tag], "solved_cnt": 0}
        for cnt, tag in solved_count:
            data[tag]["solved_cnt"] = cnt
        return data

    # 특정 티어 중에 해결 못한 문제들 반환
    def get_unsolved_by_level(self, tier, session):
        ret = []
        data = crud.read_problem_unsolved_by_tier(session, tier)
        for problem in data:
            ret.append({"id": problem.id, "title": problem.title,
                        "tier": problem.tier, "num_solved": problem.num_solved})
        return ret

    # 특정 태그 중에 해결 못한 문제들 반환
    def get_unsolved_by_tag(self, name, session):
        ret = []
        data = crud.read_problem_unsolved_by_tag(session, name)
        for problem, tag in data:
            ret.append({"id": problem.id, "title": problem.title,
                        "tier": problem.tier, "num_solved": problem.num_solved})
        return ret

    # 해당 날짜가 포함된 월~일 중에 가장 많이 푼 사람 5명 리턴
    def get_weekly_best(self, session):
        startDate, endDate = get_week_date(datetime.datetime.now())
        data = crud.read_user_after_date_order_by_num_solved(
            session, startDate)
        return data

    # 기여가 가장 많은 사람 리턴 (수정 필요)
    def get_contribute_best(self, session):
        pass
        # startDate, _ = get_week_date(
        #     datetime.datetime.now())
        # query = f"SELECT sub.name name, sum(sub.cnt) cnt FROM (SELECT name, COUNT(id) cnt, solved_at FROM solve GROUP BY id HAVING solved_at>='{startDate}') sub GROUP BY sub.name ORDER BY cnt DESC;"
        # data = self.db.executeAll(query)[:10]
        # ret = []
        # for d in data:
        #     d['cnt'] = int(d['cnt'])
        #     ret.append(d)
        # return ret


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    utility = Utility(False)

    # utility.get_problem_info()
    # utility.update_school_user()
    # utility.update_all_user_solved()
    crud.create_solve(SessionLocal(), schemas.SolveCreateWithTime(
        id=9999, name="TESTDATA3", solved_at=datetime.datetime(1900, 1, 1, 0, 0, 0)))
