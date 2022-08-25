from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..database import Base, SessionLocal
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_basic():
    result = client.get("/")
    print(result.json())
    assert 1


def test_create_experience():
    result = client.post(
        "/experience", json={"tier": 8, "exp": 20, "name": "Platinum 5"})
    result = result.json()
    assert result.get("exp") == 20
    assert result.get("name") == "Platinum 5"
    assert result.get("tier") == 8
    
    result = client.delete(
        "/experience", json={"tier":result.get("tier")}
    )


# def test_create_problem():
#     result = client.post("/problem", json={"id":1000, "title":"A+B", "tier":1,"num_solved":1000})
#     print(result)
#     pass
