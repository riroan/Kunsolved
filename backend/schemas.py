from pydantic import BaseModel
import datetime


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
    id: int
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class SolveBase(BaseModel):
    name: str
    id: int


class SolveCreate(SolveBase):
    pass


class SolveCreateWithTime(SolveBase):
    solved_at: datetime.datetime


class ContributionBase(BaseModel):
    pass


class ContributionCreate(ContributionBase):
    name: str
    id: int
