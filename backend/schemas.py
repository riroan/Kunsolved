from typing import List, Union

from pydantic import BaseModel


class ExperienceBase(BaseModel):
    tier: int
    exp: int
    name: str


class ExperienceCreate(ExperienceBase):
    pass


class ProblemBase(BaseModel):
    pass


class ProblemCreate(ProblemBase):
    id: int
    title: str
    tier: int
    num_solved: int


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
