import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = yaml.safe_load(open("config.yml"))
DATABASE_URL = config.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_recycle=10000,
                       pool_size=5, max_overflow=20, echo=False, echo_pool=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
