from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
# import .models
# import .schemas


def read_solve(db: Session, id: int, name: str):
    return db.query(models.Solve).filter(models.Solve.id == id).filter(models.Solve.name == name).first()


def read_tag(db: Session, id: int):
    return db.query(models.Tag).filter(models.Tag.id == id).all()


def read_problem(db: Session, id: int):
    return db.query(models.Problem).filter(models.Problem.id == id).first()

def read_problem_unsolved_by_tag(db:Session, tag:str):
    return db.query(models.Problem, models.Tag).filter(models.Problem.id == models.Tag.id).filter(models.Tag.name == tag).filter(~models.Problem.is_solved).all()

def read_problem_unsolved_by_tier(db:Session, tier: int):
    return db.query(models.Problem).filter(models.Problem.tier == tier).filter(~models.Problem.is_solved).all()

def read_count_solved_by_tag(db:Session, tag: str):
    return db.query(models.Solve, models.Problem, models.Tag, func.count(models.Solve.id)).distinct(models.Solve.id).filter(models.Solve.id == models.Problem.id).filter(models.Solve.id == models.Tag.id).group_by(models.Tag.name)

def read_all_problem_solved(db:Session):
    return db.query(models.Problem, models.Tag).filter(models.Problem.id == models.Tag.id).filter(models.Problem.is_solved).all()

# def read_experience(db: Session, tier_id: int):
#     return db.query(models.Experience).filter(models.Experience.tier == tier_id).first()

def read_user(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def read_all_user(db: Session):
    return db.query(models.User).all()


def create_solve(db: Session, solve: schemas.SolveCreate):
    db_solve = models.Solve(**solve.dict())
    db.add(db_solve)
    db.commit()
    db.refresh(db_solve)
    return db_solve


def create_problem(db: Session, problem: schemas.ProblemCreate):
    db_problem = models.Problem(**problem.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


# def create_experience(db: Session, experience: schemas.ExperienceCreate):
#     db_experience = models.Experience(**experience.dict())
#     db.add(db_experience)
#     db.commit()
#     # db.refresh(db_experience)
#     return db_experience


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_problem_tier(db: Session, id: int, tier: int):
    data = read_problem(db, id)
    if data:
        data.tier = tier
        db.commit()
        db.refresh(data)

def update_problem_num_solved(db: Session, id: int, num_solved: int):
    data = read_problem(db, id)
    if data:
        data.num_solved = num_solved
        db.commit()
        db.refresh(data)

def update_problem_is_solved(db:Session, id: int):
    data = read_problem(db, id)
    if data:
        data.is_solved = True
        db.commit()
        db.refresh(data)

def delete_experience(db: Session, tier: int):
    db.query(models.Experience).filter(models.Experience.tier == tier).delete()
