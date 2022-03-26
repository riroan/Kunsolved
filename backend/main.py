from typing import Optional
from fastapi import FastAPI
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
    ret = {}
    for i, v in enumerate(data):
        ret[i] = v
    return ret

@app.get("/byExp")
def byExp():
    data = util.getCountSolvedByLevel(1)
    exp = util.getAllExp()
    ret = {}
    for i, v in enumerate(zip(data, exp)):
        ret[i] = v[0]*v[1]
    return ret