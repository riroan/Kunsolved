from fastapi import FastAPI
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
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


@app.get("/byLevel")
async def byLevel():
    data = util.getCountSolvedByLevel()
    ret = dict()
    for i, v in enumerate(data):
        ret[i] = v
    util.db.commit()
    return ret


@app.get("/byExp")
async def byExp():
    data = util.getCountSolvedByLevel(1)
    exp = util.getAllExp()
    ret = dict()
    for i, v in enumerate(zip(data, exp)):
        ret[i] = v[0]*v[1]
    util.db.commit()
    return ret


@app.get("/solvedByTag")
async def solvedByTag():
    tags = ["수학", "구현", "그리디 알고리즘", "문자열",
            "자료 구조", "그래프 이론", "다이나믹 프로그래밍", "기하학"]
    outs = ["math", "implementation", "greedy", "string",
            "data_structures", "graphs", "dp", "geometry"]
    ret = dict()
    for out, tag in zip(outs, tags):
        ret[out] = len(util.getAllSolved(tag))
    util.db.commit()
    return ret

@app.get("/statusByLevel")
async def statusByLevel():
    util.db.commit()
    return util.getStatusByLevel()

@app.get("/statusByTag")
async def statusByTag():
    util.db.commit()
    return util.getStatusByTag()

@app.get("/unsolvedByLevel")
async def unsolvedByLevel(level:int):
    util.db.commit()
    return util.getUnsolvedByLevel(level)

@app.get("/unsolvedByTag")
async def unsolvedByTag(name:str):
    util.db.commit()
    return util.getUnsolvedByTag(name)


@app.get("/weeklyBest")
async def weeklyBest():
    util.db.commit()
    return util.getWeeklyBest()

@app.get("/contribBest")
async def contribBest():
    util.db.commit()
    return util.getContributeBest()

class Issue(BaseModel):
    text: str

@app.post("/issue")
async def issue(item:Issue):
    with open(f'issues/{str(datetime.datetime.now())}', 'w') as f:
        f.write(item.text)
    return {"statudCode":200}

