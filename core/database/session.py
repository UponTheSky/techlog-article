from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import config

# TODO: later chage this to async
engine = create_engine(url=config.DATABASE_URL)
session_factory = sessionmaker(bind=engine, autocommit=False)
