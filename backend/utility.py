from bs4 import BeautifulSoup
from database import Database
from tqdm import tqdm
import requests
import time
import json
import datetime

def addDays(sourceDate, count):
    targetDate = sourceDate + datetime.timedelta(days=count)
    return targetDate

def getWeekDate(sourceDate):
    temporaryDate = datetime.datetime(sourceDate.year, sourceDate.month, sourceDate.day)
    weekDayCount = temporaryDate.weekday()
    startDate = addDays(temporaryDate, -weekDayCount)
    endDate = addDays(startDate, 7)
    return str(startDate), str(endDate)

class Utility:
    def __init__(self, debug_mode = False):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        self.db = Database()
        self.debug_mode = debug_mode
    
    # 특정 유저가 해결한 문제들 반환
    def getUserInfo(self, user):  
        self.db = Database()
        url = f"https://acmicpc.net/user/{user}"
        time.sleep(2)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select('div.panel-body > div.problem-list')[0].text.strip().split(" ")
            return [int(element) for element in elements]
        else:
            return []

    # 특정 학교 구성원의 아이디 반환
    def getSchoolInfo(self, number, page=1):
        self.db = Database()
        url = f"https://www.acmicpc.net/school/ranklist/{number}/{page}"
        response = requests.get(url, headers=self.headers)
        time.sleep(2)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            users = soup.select('#ranklist tr > td:nth-child(2) a')
            return [user.text for user in users]
        else:
            return []
    
    # 특정 학교 구성원이 최근에 해결한 문제 반환
    def getRecentSolved(self, number):
        self.db = Database()
        url = f"https://www.acmicpc.net/status?school_id={number}"
        response = requests.get(url, headers=self.headers)
        time.sleep(2)
        if response.status_code==200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            users = soup.select('#status-table > tbody > tr > td:nth-child(2) > a')
            
            users = [user.text for user in users]
            
            problems = soup.select(
                '#status-table > tbody > tr > td:nth-child(3) > a')
            problems = [problem.text for problem in problems]
            status = soup.select(
                '#status-table > tbody > tr > td:nth-child(4) > span')
            status = [st.text for st in status if st.text !='\xa0']
            ret_user, ret_problem = [], []
            for user, problem, st in zip(users, problems, status):
                if st == "맞았습니다!!":
                    ret_user.append(user)
                    ret_problem.append(problem)
            return ret_user, ret_problem
        else:
            return [], []
        
    def addRecentSolved(self, number):
        self.db = Database()
        users, problems = self.getRecentSolved(number)
        for user, problem in zip(users, problems):
            query = f'SELECT * FROM solve WHERE id={problem} AND name="{user}"'
            data = self.db.executeOne(query)
            if data is None:
                query = f'INSERT INTO solve (name, id) VALUES ("{user}", {problem});'
                try:
                    self.db.execute(query)
                except Exception:
                    pass
        self.db.commit()

    # 존재하는 모든 문제 아이디, 제목을 db에 추가
    def getProblemInfo(self):
        self.db = Database()
        ix = 1
        while True:
            url = f"https://solved.ac/api/v3/search/problem?query=solvable:true&page={ix}"
            time.sleep(2)
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
                title = title.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("%", "%%")
                level = problem['level']
                try:
                    query = f'INSERT INTO problem (id, title, tier) VALUES ({number}, \"{title}\", {level});'
                    self.db.execute(query)
                    for tag in problem['tags']:
                        t = tag['displayNames'][-1]['name']
                        query = f'INSERT INTO tag (id, name) VALUES ({number}, \"{t}\");'
                        self.db.execute(query)
                except Exception:
                    if self.debug_mode:
                        print(f">> Warning : Problem {number} is already existed")
                    continue
            ix += 1
        self.db.commit()


    # 특정 학교에 존재하는 모든 유저 아이디 반환
    def getAllUser(self, number):
        self.db = Database()
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
    def updateSchoolUser(self, number):
        self.db = Database()
        users = self.getAllUser(number)
        for user in users:
            try:
                self.db.execute(f"INSERT INTO school (name) VALUES ('{user}');")
            except Exception:
                if self.debug_mode:
                    print(f">> Warning : User {user} is already existed")
        self.db.commit()

    # 특정 학교에 존재하는 모든 유저의 해결한 문제 업데이트
    def updateAllUserSolved(self):
        self.db = Database()
        query = f"select * from school;"
        users = self.db.executeAll(query)
        users = [user["name"] for user in users]
        for user in tqdm(users):
            solved = self.getUserInfo(user)
            for solve in solved:
                query = f"SELECT * FROM solve WHERE name = '{user}' AND id = '{solve}';"
                data = self.db.executeOne(query)
                if data:
                    if self.debug_mode:
                        print(
                            f">> Warning : Problem {solve} solved by {user} is already existed")
                    continue
                query = f"INSERT INTO solve (name, id) VALUES ('{user}', {solve});"
                self.db.execute(query)
        self.db.commit()

    # 특정 학교 구성원이 해결한 모든 문제 반환
    def getAllSolved(self, tag=""):
        self.db = Database()
        if tag=="":
            query = "SELECT DISTINCT solve.id, problem.tier FROM solve, problem WHERE solve.id = problem.id;"
        else:
            query = f"SELECT DISTINCT solve.id, problem.tier FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id AND tag.name='{tag}';"
        data = self.db.executeAll(query)
        return data

    # 특정 학교 구성원이 해결한 모든 문제를 난이도별 개수로 반환
    def getCountSolvedByLevel(self, verbose=0):
        self.db = Database()
        query = "SELECT problem.tier, COUNT(DISTINCT solve.id) cnt FROM solve, problem WHERE solve.id = problem.id GROUP BY problem.tier ORDER BY problem.tier;"
        data = self.db.executeAll(query)
        if verbose == 0: # 브론즈, 실버, 골드...
            NUM_TIER = 7
            cnt = [0] * NUM_TIER
            for d in data:
                cnt[(d['tier']+4)//5] += d['cnt']
        elif verbose == 1: # 브론즈5, 브론즈4, 브론즈3, ...
            NUM_TIER = 31
            cnt = [0] * NUM_TIER
            for d in data:
                cnt[d['tier']] += d['cnt']
        return cnt

    def getCountAllSolvedByTag(self):
        self.db = Database()
        query = "SELECT tag.name, COUNT(DISTINCT solve.id) cnt FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id GROUP BY tag.name;"
        data = self.db.executeAll(query)
        ret = dict()
        for d in data:
            ret[d['name']] = d['cnt']
        return ret

    def getCountSolvedByTag(self, tag):
        self.db = Database()
        # query = f'SELECT DISTINCT solve.id, tag.name FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id AND tag.name="{tag}";'
        # data = self.db.executeAll(query)
        # return [d["id"] for d in data]
        try:
            return self.getCountAllSolvedByTag()[tag]
        except KeyError:
            return 0
    
    def getAllExp(self):
        self.db = Database()
        query = "SELECT * FROM experience;"
        data = self.db.executeAll(query)
        NUM_TIER = 31
        ret = [0]*NUM_TIER
        for d in data:
            ret[d['tier']] = d['exp']
        return ret
    
    def getStatusByLevel(self):
        self.db = Database()
        query = "SELECT COUNT(p.tier) cnt, e.name, e.tier FROM problem p, experience e WHERE p.tier = e.tier GROUP BY p.tier;"
        all_count = self.db.executeAll(query)
        
        query = "SELECT COUNT(distinct solve.id) cnt, problem.tier FROM solve, problem WHERE solve.id = problem.id GROUP BY problem.tier;"
        solved_count = self.db.executeAll(query)
        
        data = {}
        for d in all_count:
            data[d['tier']] = {'name':d['name'], 'all_cnt':d['cnt'], 'solved_cnt':0}
        for d in solved_count:
            data[d['tier']]['solved_cnt'] = d['cnt']
        
        return data
    
    def getStatusByTag(self):
        self.db = Database()
        query = "SELECT COUNT(t.name) cnt, t.name FROM problem p, tag t WHERE p.id = t.id GROUP BY t.name ORDER BY cnt DESC;"
        all_count = self.db.executeAll(query)
        
        query = "SELECT COUNT(distinct problem.id) cnt, tag.name FROM solve, problem, tag WHERE solve.id = problem.id AND problem.id = tag.id GROUP BY tag.name;"
        solved_count = self.db.executeAll(query)
        
        data = {}
        for d in all_count:
            data[d['name']] = {'all_cnt':d['cnt'], 'solved_cnt':0}
        for d in solved_count:
            data[d['name']]['solved_cnt'] = d['cnt']
        return data
    
    # 특정 티어 중에 해결 못한 문제들 반환
    def getUnsolvedByLevel(self, tier):
        self.db = Database()
        query = f"SELECT DISTINCT solve.id, experience.tier FROM solve, problem, experience WHERE solve.id = problem.id AND problem.tier = experience.tier AND experience.tier = {tier};"
        solved = self.db.executeAll(query)
        solved = [item['id'] for item in solved]
        query = f"SELECT * FROM problem WHERE tier={tier};"
        all_data = self.db.executeAll(query)
        unsolved = []
        for d in all_data:
            if d['id'] not in solved:
                unsolved.append(d)
        data = {}
        for d in unsolved:
            data[d['id']] = d['title']
        return data
    
    # 특정 태그 중에 해결 못한 문제들 반환
    def getUnsolvedByTag(self, name):
        self.db = Database()
        query = f'SELECT DISTINCT solve.id, tag.name FROM solve, problem, tag WHERE solve.id = problem.id AND problem.id = tag.id AND tag.name = "{name}";'
        solved = self.db.executeAll(query)
        solved = [item['id'] for item in solved]
        query = f'SELECT * FROM tag, problem WHERE tag.id = problem.id AND tag.name = "{name}" ORDER BY problem.tier'
        all_data = self.db.executeAll(query)
        unsolved = []
        for d in all_data:
            if d['id'] not in solved:
                unsolved.append(d)
        data = {}
        for d in unsolved:
            data[d['id']] = {"title":d['title'], "tier":d["tier"]}
        return data
    
    # 해당 날짜가 포함된 월~일 중에 가장 많이 푼 사람 5명 리턴
    def getWeeklyBest(self):
        self.db = Database()
        startDate, endDate = getWeekDate(datetime.datetime.now() - datetime.timedelta(hours=-9))
        query = f"SELECT name, COUNT(id) cnt FROM solve WHERE solved_at >= '{startDate}' AND solved_at <= '{endDate}' GROUP BY name;"
        data = self.db.executeAll(query)
        data.sort(key=lambda x : x['cnt'], reverse = True)
        return data[:10]

if __name__ == "__main__":
    utility = Utility(True)
    data = utility.getWeeklyBest()
    print(data)