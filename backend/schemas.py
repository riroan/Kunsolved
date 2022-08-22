from typing import List, Union

from pydantic import BaseModel


class ExperienceBase(BaseModel):
    tier: int
    name: str
    exp: int


class ExperienceCreate(ExperienceBase):
    pass


class Experience(ExperienceBase):
    class Config:
        orm_mode = True

class ProblemBase(BaseModel):
    id: int
    title: str
    tier: int
    num_solved: int


class ProblemCreate(ProblemBase):
    pass

class Problem(ProblemBase):
    is_solved: bool
    class Config:
        orm_mode = True

class TagBase(BaseModel):
    pass


class TagCreate(TagBase):
    id: int
    name: str


class SchoolBase(BaseModel):
    name: str


class SchoolCreate(SchoolBase):
    pass


class SolveBase(BaseModel):
    pass


class SolveCreate(SolveBase):
    name: str
    id: int
