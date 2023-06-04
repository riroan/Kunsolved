from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Problem, Tag, User, Solve
import schemas


def read_solve(db: Session, id: int, name: str):
    return db.query(Solve).filter(Solve.id == id).filter(Solve.name == name).first()


def read_tag(db: Session, id: int):
    return db.query(Tag).filter(Tag.id == id).all()


def read_problem(db: Session, id: int):
    return db.query(Problem).filter(Problem.id == id).first()


def read_problem_unsolved_by_tag(db: Session, tag: str):
    return db.query(Problem, Tag).filter(Problem.id == Tag.id).filter(Tag.name == tag).filter(~Problem.is_solved).all()


def read_problem_unsolved_by_tier(db: Session, tier: int):
    return db.query(Problem).filter(Problem.tier == tier).filter(~Problem.is_solved).all()


def read_problem_solved_by_tag(db: Session, tag: str):
    return db.query(Problem, Tag).filter(Problem.id == Tag.id).filter(Problem.is_solved).filter(Tag.name == tag).all()


def read_all_problem_solved(db: Session):
    return db.query(Problem).filter(Problem.is_solved).distinct().all()


def read_user(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def read_all_user(db: Session):
    return db.query(User).all()


def read_user_after_date_order_by_num_solved(db: Session, date: str, limit: int = 10):
    return db.query(func.count(Solve.id), Solve.name).filter(Solve.solved_at >= date).order_by(func.count(Solve.id).desc()).group_by(Solve.name).limit(limit).all()


def read_all_problem_count_by_tag(db: Session):
    return db.query(func.count(Tag.name), Tag.name).filter(Problem.id == Tag.id).group_by(Tag.name).order_by(func.count(Tag.name).desc()).all()


def read_problem_solved_count_by_tag(db: Session):
    subquery = db.query(Solve.id).group_by(Solve.id).subquery()
    return db.query(func.count(Tag.name), Tag.name).filter(Tag.id == subquery.c.id).group_by(Tag.name).all()


def read_all_problem_count_by_tier(db: Session):
    return db.query(func.count(Problem.tier), Problem.tier).group_by(Problem.tier).all()


def read_problem_solved_count_by_tier(db: Session):
    subquery = db.query(Solve.id).group_by(Solve.id).subquery()
    return db.query(func.count(Problem.tier), Problem.tier).filter(Problem.id == subquery.c.id).group_by(Problem.tier).order_by(Problem.tier.asc()).all()


def create_solve(db: Session, solve: schemas.SolveCreate):
    db_solve = Solve(**solve.dict())
    db.add(db_solve)
    db.commit()
    db.refresh(db_solve)
    return db_solve


def create_problem(db: Session, problem: schemas.ProblemCreate):
    db_problem = Problem(**problem.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.dict())
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


def update_problem_is_solved(db: Session, id: int):
    data = read_problem(db, id)
    if data:
        data.is_solved = True
        db.commit()
        db.refresh(data)
