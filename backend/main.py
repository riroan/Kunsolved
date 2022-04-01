from typing import Optional, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utility import Utility
import asyncio

app = FastAPI()
util = Utility()

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/byLevel")
async def byLevel():
    data = util.getCountSolvedByLevel()
    ret = dict()
    for i, v in enumerate(data):
        ret[i] = v
    return ret


@app.get("/byExp")
async def byExp():
    data = util.getCountSolvedByLevel(1)
    exp = util.getAllExp()
    ret = dict()
    for i, v in enumerate(zip(data, exp)):
        ret[i] = v[0]*v[1]
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
    return ret

@app.get("/statusByLevel")
async def statusByLevel():
    return util.getStatusByLevel()

@app.get("/statusByTag")
async def statusByTag():
    return util.getStatusByTag()

@app.get("/unsolvedByLevel")
async def unsolvedByLevel(level:int):
    return util.getUnsolvedByLevel(level)

@app.get("/unsolvedByTag")
async def unsolvedByTag(name:str):
    return util.getUnsolvedByTag(name)