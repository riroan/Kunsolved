from bs4 import BeautifulSoup
from database import Database
from tqdm import tqdm
import requests
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def getUserInfo(user):
    url = f"https://acmicpc.net/user/{user}"
    time.sleep(2)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select('div.panel-body > div.problem-list')[0].text.strip().split(" ")
        return [int(element) for element in elements]
    else:
        return []

def getSchoolInfo(number, page=1):
    url = f"https://www.acmicpc.net/school/ranklist/{number}/{page}"
    response = requests.get(url, headers=headers)
    time.sleep(2)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        users = soup.select('#ranklist tr > td:nth-child(2) a')
        return [user.text for user in users]
    else:
        return []


def getProblemInfo():
    ix = 1
    while True:
        print(ix)
        url = f"https://solved.ac/api/v3/search/problem?query=solvable:true&page={ix}"
        time.sleep(2)
        response = requests.get(url)
        try:
            items = json.loads(response.text)
        except:
            print(response.text)
            assert 0
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
                db.execute(query)
                for tag in problem['tags']:
                    t = tag['displayNames'][-1]['name']
                    query = f'INSERT INTO tag (id, name) VALUES ({number}, \"{t}\");'
                    db.execute(query)
            except:
                print(query, title)
                assert 0
        ix += 1
    db.commit()


def getAllUser(number):
    ix = 1
    users = []
    while True:
        info = getSchoolInfo(number, ix)
        if len(info) == 0:
            break
        users.extend(info)
        ix += 1
    return users


def updateSchoolUser(number):
    users = getAllUser(number)
    for user in users:
        try:
            db.execute(f"INSERT INTO school (name) VALUES ('{user}');")
        except Exception:
            pass
    db.commit()

def updateAllUserSolved():
    query = f"select * from school;"
    users = db.executeAll(query)
    users = [user["name"] for user in users]
    for user in tqdm(users):
        solved = getUserInfo(user)
        for solve in solved:
            query = f"INSERT INTO solve (name, id) VALUES ('{user}', {solve});"
            db.execute(query)
    db.commit()

def getAllSolved():
    pass


db = Database()
# updateSchoolUser(194)
# print(getUserInfo("riroan"))
# getProblemInfo()
# number = 17366
# title = "\\\\"
# level = 25
# query = f'INSERT INTO problem (id, title, tier) VALUES ({number}, \"{title}\", {level});'

# db.execute(query)
updateAllUserSolved()

