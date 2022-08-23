from bs4 import BeautifulSoup
from database import Database, SessionLocal, engine
from tqdm import tqdm

import requests
import time
import json
import datetime
import crud
import schemas
import models


def addDays(sourceDate, count):
    targetDate = sourceDate + datetime.timedelta(days=count)
    return targetDate


def getWeekDate(sourceDate):
    temporaryDate = datetime.datetime(
        sourceDate.year, sourceDate.month, sourceDate.day)
    weekDayCount = temporaryDate.weekday()
    startDate = addDays(temporaryDate, -weekDayCount)
    endDate = addDays(startDate, 7)
    return str(startDate), str(endDate)


class Utility:
    def __init__(self, debug_mode=False):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        self.debug_mode = debug_mode
        self.session = SessionLocal()

    def log(self, message):
        now = now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print(f">> Log ({now}): {message}")

    # 특정 유저가 해결한 문제들 반환
    def getUserInfo(self, user):
        url = f"https://acmicpc.net/user/{user}"
        time.sleep(3)
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
    def getSchoolInfo(self, number, page=1):
        url = f"https://www.acmicpc.net/school/ranklist/{number}/{page}"
        response = requests.get(url, headers=self.headers)
        time.sleep(5)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            users = soup.select('#ranklist tr > td:nth-child(2) a')
            return [user.text for user in users]
        else:
            return []

    # 특정 학교 구성원이 최근에 해결한 문제 반환
    def getRecentSolved(self, number=194):
        self.log("getRecentSolved")
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

    def addRecentSolved(self, number=194):
        self.log("addRecentSolved")
        users, problems = self.getRecentSolved(number)
        for user, problem_id in zip(users, problems):
            # query = f'SELECT * FROM solve WHERE id={problem} AND name="{user}"'
            # data = self.db.executeOne(query)
            data = crud.read_solve(self.session, problem_id, user)
            if data is None:
                try:
                    # query = f'INSERT INTO solve (name, id) VALUES ("{user}", {problem});'
                    # self.db.execute(query)
                    crud.create_solve(self.session, schemas.SolveCreate(
                        name=user, id=problem_id))
                    # query = f'UPDATE problem SET is_solved=true WHERE id={problem};'
                    # self.db.execute(query)
                except Exception:
                    pass
        # self.db.commit()

    # 존재하는 모든 문제 아이디, 제목을 db에 추가 이미 있으면 태그, 티어 업데이트
    def getProblemInfo(self):
        self.log("getProblemInfo")
        ix = 1
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
                    crud.create_problem(self.session, schemas.ProblemCreate(
                        id=number, title=title, tier=level, num_solved=num_solved))
                    for tag in tags:
                        for displayNames in tag['displayNames']:
                            if displayNames['language'] == 'ko':
                                t = displayNames['name']
                        crud.create_tag(
                            self.session, schemas.TagCreate(id=number, name=t))
                except Exception:
                    if self.debug_mode:
                        print(f">> Problem {number} is already existed")
                    self.session.rollback()
                    crud.update_problem_tier(self.session, number, level)
                    existed = crud.read_tag(self.session, number)
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
                                self.session, schemas.TagCreate(id=number, name=v))
                        if self.debug_mode:
                            print(f">> Problem {number}'s tag is updated")
                    crud.update_problem_num_solved(self.session, number, num_solved)
            ix += 1
            print(ix)

    # 특정 학교에 존재하는 모든 유저 아이디 반환
    def getAllUser(self, number):
        ix = 1
        users = []
        while True:
            info = self.getSchoolInfo(number, ix)
            if len(info) == 0:
                break
            users.extend(info)
            ix += 1
        return users

    # 특정 학교에 존재하는 모든 유저 아이디 db에 추가
    def updateSchoolUser(self, number=194):
        self.log("updateSchoolUser")
        users = self.getAllUser(number)
        
        for user in users:
            try:
                crud.create_user(self.session, schemas.UserCreate(name=user))
            # break
                # self.db.execute(
                #     f"INSERT INTO school (name) VALUES ('{user}');")
            except Exception:
                self.session.rollback()
                if self.debug_mode:
                    print(f">> Warning : User {user} is already existed")
        # self.db.commit()

    # 특정 학교에 존재하는 모든 유저의 해결한 문제 업데이트
    def updateAllUserSolved(self):
        self.log("updateAllUserSolved")
        users = crud.read_all_user(self.session)
        users = [user.name for user in users]
        for user in tqdm(users):
            solved = self.getUserInfo(user)
            for solve in solved:
                data = crud.read_solve(self.session, solve, user)
                if data:
                    if self.debug_mode:
                        print(
                            f">> Warning : Problem {solve} solved by {user} is already existed")
                    continue
                crud.create_solve(self.session, schemas.SolveCreate(name = user, id = solve))
                crud.update_problem_is_solved(self.session, solve)
                if self.debug_mode:
                    print(
                        f">> Log : Problem {solve} solved by {user} is appended")

    # 특정 학교 구성원이 해결한 모든 문제 반환
    def getAllSolved(self, tag=""):
        # if tag == "":
        #     query = "SELECT problem.id, problem.tier, tag.name FROM problem, tag WHERE problem.id=tag.id AND problem.is_solved = true;"
        # else:
        #     query = f"SELECT problem.id, problem.tier FROM problem, tag WHERE problem.id = tag.id AND problem.is_solved=true AND tag.name='{tag}';"
        # data = self.db.executeAll(query)
        data = crud.read_all_problem_solved(self.session)
        return data

    # 특정 학교 구성원이 해결한 모든 문제를 난이도별 개수로 반환
    def getCountSolvedByLevel(self, verbose=0):
        query = "SELECT problem.tier, COUNT(DISTINCT solve.id) cnt FROM solve, problem WHERE solve.id = problem.id GROUP BY problem.tier ORDER BY problem.tier;"
        data = self.db.executeAll(query)
        if verbose == 0:  # 브론즈, 실버, 골드...
            NUM_TIER = 7
            cnt = [0] * NUM_TIER
            for d in data:
                cnt[(d['tier']+4)//5] += d['cnt']
        elif verbose == 1:  # 브론즈5, 브론즈4, 브론즈3, ...
            NUM_TIER = 31
            cnt = [0] * NUM_TIER
            for d in data:
                cnt[d['tier']] += d['cnt']
        return cnt

    def getCountAllSolvedByTag(self):
        # query = "SELECT tag.name, COUNT(DISTINCT solve.id) cnt FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id GROUP BY tag.name;"
        # data = self.db.executeAll(query)
        data = crud.read_count_solved_by_tag(self.session, "수학") # 수정 필요
        print(data)
        assert 0
        ret = dict()
        for d in data:
            ret[d['name']] = d['cnt']
        return ret

    def getCountSolvedByTag(self, tag):
        # query = f'SELECT DISTINCT solve.id, tag.name FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id AND tag.name="{tag}";'
        # data = self.db.executeAll(query)
        # return [d["id"] for d in data]
        try:
            return self.getCountAllSolvedByTag()[tag]
        except KeyError:
            return 0

    def getAllExp(self):
        query = "SELECT * FROM experience;"
        data = self.db.executeAll(query)
        NUM_TIER = 31
        ret = [0]*NUM_TIER
        for d in data:
            ret[d['tier']] = d['exp']
        return ret

    def getStatusByLevel(self):
        query = "SELECT COUNT(p.tier) cnt, e.name, e.tier FROM problem p, experience e WHERE p.tier = e.tier GROUP BY p.tier;"
        all_count = self.db.executeAll(query)

        query = "SELECT COUNT(distinct solve.id) cnt, problem.tier FROM solve, problem WHERE solve.id = problem.id GROUP BY problem.tier;"
        solved_count = self.db.executeAll(query)

        data = {}
        for d in all_count:
            data[d['tier']] = {'name': d['name'],
                               'all_cnt': d['cnt'], 'solved_cnt': 0}
        for d in solved_count:
            data[d['tier']]['solved_cnt'] = d['cnt']
        return data

    def getStatusByTag(self):
        query = "SELECT COUNT(t.name) cnt, t.name FROM problem p, tag t WHERE p.id = t.id GROUP BY t.name ORDER BY cnt DESC;"
        all_count = self.db.executeAll(query)

        # query = "SELECT COUNT(distinct problem.id) cnt, tag.name FROM solve, problem, tag WHERE solve.id = problem.id AND problem.id = tag.id GROUP BY tag.name;"
        query = "SELECT COUNT(distinct t.id) cnt, t.name FROM tag t, (SELECT id FROM solve GROUP BY id) p WHERE p.id = t.id GROUP BY t.name;"
        solved_count = self.db.executeAll(query)

        data = {}
        for d in all_count:
            data[d['name']] = {'all_cnt': d['cnt'], 'solved_cnt': 0}
        for d in solved_count:
            data[d['name']]['solved_cnt'] = d['cnt']
        return data

    # 특정 티어 중에 해결 못한 문제들 반환
    def getUnsolvedByLevel(self, tier):
        # query = f"SELECT * FROM problem WHERE is_solved = false AND tier={tier};"
        # data = self.db.executeAll(query)
        data = crud.read_problem_unsolved_by_tier(self.session, tier)
        ret = []
        for problem in data:
            ret.append({"id": problem.id, "title": problem.title,
                       "tier": problem.tier, "num_solved": problem.num_solved})
        return ret

    # 특정 태그 중에 해결 못한 문제들 반환
    def getUnsolvedByTag(self, name):
        data = crud.read_problem_unsolved_by_tag(self.session, name)
        # query = f"SELECT * FROM problem, tag WHERE problem.id = tag.id AND problem.is_solved = false AND tag.name='{name}';"
        # data = self.db.executeAll(query)
        ret = []
        for problem, tag in data:
            ret.append({"id": problem.id, "title": problem.title,
                       "tier": problem.tier, "num_solved": problem.num_solved})
        return ret

    # 해당 날짜가 포함된 월~일 중에 가장 많이 푼 사람 5명 리턴
    def getWeeklyBest(self):
        startDate, endDate = getWeekDate(datetime.datetime.now())

        query = f"SELECT name, COUNT(id) cnt FROM solve WHERE solved_at >= '{startDate}' GROUP BY name ORDER BY cnt DESC;"
        data = self.db.executeAll(query)[:10]
        return data

    # 기여가 가장 많은 사람 리턴 (수정 필요)
    def getContributeBest(self):
        startDate, _ = getWeekDate(
            datetime.datetime.now())
        query = f"SELECT sub.name name, sum(sub.cnt) cnt FROM (SELECT name, COUNT(id) cnt, solved_at FROM solve GROUP BY id HAVING solved_at>='{startDate}') sub GROUP BY sub.name ORDER BY cnt DESC;"
        data = self.db.executeAll(query)[:10]
        ret = []
        for d in data:
            d['cnt'] = int(d['cnt'])
            ret.append(d)
        return ret


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    utility = Utility(True)
    # data = utility.getWeeklyBest()
    # utility.getAllUser(194)
    # utility.getProblemInfo()
    # print(utility.addRecentSolved())
    # utility.updateSchoolUser()
    # utility.getProblemInfo()
    # utility.updateAllUserSolved()
    # data = utility.getUnsolvedByLevel(3)
    # print(data)
    # print(crud.read_problem_unsolved_by_tag())
    # print(utility.getCountSolvedByTag("수학"))
    utility.getAllSolved()
