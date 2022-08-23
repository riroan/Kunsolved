from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


# class Experience(Base):
#     __tablename__ = "experience"

#     tier = Column(Integer, primary_key=True, index=True, autoincrement=False)
#     exp = Column(Integer)
#     name = Column(String(15))

#     r_problem = relationship("Problem", back_populates="r_experience")


class Problem(Base):
    __tablename__ = "problem"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    tier = Column(Integer)
    is_solved = Column(Boolean, default=False)
    num_solved = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    r_solve = relationship("Solve", back_populates="r_problem")
    r_tag = relationship("Tag", back_populates="r_problem")


class Tag(Base):
    __tablename__ = "tag"

    idx = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, ForeignKey("problem.id"))
    name = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    r_problem = relationship("Problem", back_populates="r_tag")


class User(Base):
    __tablename__ = "users"

    name = Column(String(25), unique=True, index=True, primary_key=True)
    created_at = Column(DateTime, default=func.now())

    r_solve = relationship("Solve", back_populates="r_users")


class Solve(Base):
    __tablename__ = "solve"

    idx = Column(Integer, primary_key=True)
    name = Column(String(25), ForeignKey("users.name"))
    id = Column(Integer, ForeignKey("problem.id"))
    solved_at = Column(DateTime, default=func.now())

    r_users = relationship("User", back_populates="r_solve")
    r_problem = relationship("Problem", back_populates="r_solve")
