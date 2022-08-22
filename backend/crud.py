from sqlalchemy.orm import Session
from . import models, schemas
# import .models
# import .schemas


def get_solve(db: Session, id: int, name: str):
    return db.query(models.Solve).filter(models.Solve.id == id).filter(models.Solve.name == name).first()


def get_tag(db: Session, id: int):
    return db.query(models.Tag).filter(models.Tag.id == id).all()


def get_problem(db: Session, id: int):
    return db.query(models.Problem).filter(models.Problem.id == id).first()


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

def create_experience(db: Session, experience: schemas.ExperienceCreate):
    db_experience = models.Experience(**experience.dict())
    db.add(db_experience)
    db.commit()
    # db.refresh(db_experience)
    return db_experience

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_experience(db: Session, tier: int):
    db.query(models.Experience).filter(models.Experience.tier == tier).delete()