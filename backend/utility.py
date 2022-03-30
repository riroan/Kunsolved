from bs4 import BeautifulSoup
from database import Database
from tqdm import tqdm
import requests
import time
import json
import asyncio

class Utility:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        self.db = Database()

    # 특정 유저가 해결한 문제들 반환
    def getUserInfo(self, user):  
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

    # 존재하는 모든 문제 아이디, 제목을 db에 추가
    def getProblemInfo(self):
        ix = 1
        while True:
            url = f"https://solved.ac/api/v3/search/problem?query=solvable:true&page={ix}"
            time.sleep(2)
            response = requests.get(url)
            try:
                items = json.loads(response.text)
            except:
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
                except:
                    print(query, title)
                    continue
            ix += 1
        self.db.commit()


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
    def updateSchoolUser(self, number):
        users = self.getAllUser(number)
        for user in users:
            try:
                self.db.execute(f"INSERT INTO school (name) VALUES ('{user}');")
            except Exception:
                pass
        self.db.commit()

    # 특정 학교에 존재하는 모든 유저의 해결한 문제 업데이트
    def updateAllUserSolved(self):
        query = f"select * from school;"
        users = self.db.executeAll(query)
        users = [user["name"] for user in users]
        for user in tqdm(users):
            solved = self.getUserInfo(user)
            for solve in solved:
                query = f"INSERT INTO solve (name, id) VALUES ('{user}', {solve});"
                self.db.execute(query)
        self.db.commit()

    # 특정 학교 구성원이 해결한 모든 문제 반환
    def getAllSolved(self, tag=""):
        if tag=="":
            query = "SELECT DISTINCT solve.id, problem.tier FROM solve, problem WHERE solve.id = problem.id;"
        else:
            query = f"SELECT DISTINCT solve.id, problem.tier FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id AND tag.name='{tag}';"
        data = self.db.executeAll(query)
        return data

    # 특정 학교 구성원이 해결한 모든 문제를 난이도별 개수로 반환
    def getCountSolvedByLevel(self, verbose=0):
        query = "SELECT problem.tier, COUNT(DISTINCT solve.id) cnt  FROM solve, problem WHERE solve.id = problem.id GROUP BY problem.tier ORDER BY problem.tier;"
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
        query = "SELECT tag.name, COUNT(DISTINCT solve.id) cnt FROM solve, problem, tag WHERE solve.id = problem.id AND solve.id = tag.id GROUP BY tag.name;"
        data = self.db.executeAll(query)
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

# print(getCountSolvedByLevel(1))
# print(getCountSolvedByLevel())
# updateSchoolUser(194)
# print(getUserInfo("riroan"))
# getProblemInfo()
# number = 17366
# title = "\\\\"
# level = 25
# query = f'INSERT INTO problem (id, title, tier) VALUES ({number}, \"{title}\", {level});'

# db.execute(query)
# updateAllUserSolved()

if __name__ == "__main__":
    utility = Utility()
    print(utility.getAllExp())