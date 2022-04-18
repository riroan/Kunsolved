from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utility import Utility
import datetime

app = FastAPI()
util = Utility()

origins = [
    "http://localhost:3000",
    "https://bj.riroan.com",
    "https://www.bj.riroan.com",
    "http://www.bj.riroan.com",
    "http://www.bj.riroan.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


@app.get("/v1/level")
async def byLevel():
    data = util.getCountSolvedByLevel()
    ret = dict()
    for i, v in enumerate(data):
        ret[i] = v
    util.db.commit()
    return ret


@app.get("/v1/exp")
async def byExp():
    data = util.getCountSolvedByLevel(1)
    exp = util.getAllExp()
    ret = dict()
    for i, v in enumerate(zip(data, exp)):
        ret[i] = v[0]*v[1]
    util.db.commit()
    return ret


@app.get("/v1/tag")
async def solvedByTag():
    d = {"수학": "math", "구현": "implementation", "그리디 알고리즘": "greedy", "문자열": "string", "자료 구조": "data_structures",
         "그래프 이론": "graphs", "다이나믹 프로그래밍": "dp", "기하학": "geometry"}
    ret = dict()
    for tag in d.values():
        ret[tag] = 0
    for i in util.getAllSolved():
        try:
            ret[d[i['name']]] += 1
        except:
            pass
    util.db.commit()
    return ret


@app.get("/v1/status/level")
async def statusByLevel():
    util.db.commit()
    return util.getStatusByLevel()


@app.get("/v1/status/tag")
async def statusByTag():
    util.db.commit()
    return util.getStatusByTag()


@app.get("/v1/unsolved/level")
async def unsolvedByLevel(level: int):
    util.db.commit()
    return util.getUnsolvedByLevel(level)


@app.get("/v1/unsolved/tag")
async def unsolvedByTag(name: str):
    util.db.commit()
    return util.getUnsolvedByTag(name)


@app.get("/v1/best/week")
async def weeklyBest():
    util.db.commit()
    return util.getWeeklyBest()


@app.get("/v1/best/contrib")
async def contribBest():
    util.db.commit()
    return util.getContributeBest()


class Issue(BaseModel):
    text: str


@app.post("/v1/issue", status_code=status.HTTP_201_CREATED)
async def issue(item: Issue):
    with open(f'issues/{str(datetime.datetime.now())}', 'w') as f:
        f.write(item.text)
    return {"statudCode": 200}
