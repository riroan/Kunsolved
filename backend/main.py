from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from utility import Utility
from database import SessionLocal, engine
import schemas
import crud
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


@app.get("/v1/level")
async def byLevel():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/level")
    data = util.getProblemSolvedByLevel()
    return data


@app.get("/v1/exp")
async def byExp():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/exp")
    data = util.getCountSolvedByLevel(1)
    exp = util.getAllExp()
    ret = dict()
    for i, v in enumerate(zip(data, exp)):
        ret[i] = v[0]*v[1]
    util.db.commit()
    return ret


@app.get("/v1/tag")
async def solvedByTag():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/tag")
    d = {"수학": "math", "구현": "implementation", "그리디 알고리즘": "greedy", "문자열": "string", "자료 구조": "data_structures",
         "그래프 이론": "graphs", "다이나믹 프로그래밍": "dp", "기하학": "geometry"}
    ret = dict()
    for tag in d:
        data = util.getProblemSolvedByTag(tag)
        ret[d[tag]] = len(data)

    return ret


@app.get("/v1/status/level")
async def statusByLevel():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/status/level")
    return util.getStatusByLevel()


@app.get("/v1/status/tag")
async def statusByTag():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/status/tag")
    return util.getStatusByTag()


@app.get("/v1/unsolved/level")
async def unsolvedByLevel(level: int):
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/unsolved/level")
    return util.getUnsolvedByLevel(level)


@app.get("/v1/unsolved/tag")
async def unsolvedByTag(name: str):
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/unsolved/tag")
    return util.getUnsolvedByTag(name)


@app.get("/v1/best/week")
async def weeklyBest():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/best/week")
    data = util.getWeeklyBest()
    data = [{"cnt": d[0], "name":d[1]} for d in data]
    return data


@app.get("/v1/best/contrib")
async def contribBest():
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/best/contrib")
    return util.getContributeBest()


class Issue(BaseModel):
    text: str


@app.post("/v1/issue", status_code=status.HTTP_201_CREATED)
async def issue(item: Issue):
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f">> Log ({now}) : /v1/issue")
    with open(f'issues/{str(datetime.datetime.now())}', 'w') as f:
        f.write(item.text)
    return {"statudCode": 200}
