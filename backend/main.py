from typing import Optional, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utility import Utility

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
def read_root():
    return {"Hello":"World"}

@app.get("/byLevel")
def byLevel():
    data = util.getCountSolvedByLevel()
    ret = dict()
    for i, v in enumerate(data):
        ret[i] = v
    return ret

@app.get("/byExp")
def byExp():
    data = util.getCountSolvedByLevel(1)
    exp = util.getAllExp()
    ret = dict()
    for i, v in enumerate(zip(data, exp)):
        ret[i] = v[0]*v[1]
    return ret

@app.get("/byTag")
def byTag(tags:List[str] = Query([""]), value:str = "exp"):
    print(tags, type(tags), value)
    if value == "exp":
        exp = util.getAllExp()
        ret = dict()
        for tag in tags:
            print(tag)
            problem = util.getAllSolved(tag)
            e = 0
            for p in problem:
                tier = p["tier"]
                e+=exp[tier]
            ret[tag] = e
        return ret
    elif value == "cnt":
        ret = dict()
        tag = tags[0]
        data = util.getAllSolved(tag)
        ret[tag] = len(data)
        return ret
    else:
        return {"detail":"Not Found"}