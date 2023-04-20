from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from ..config import config


engine = create_engine(url=config.DB_URL)
session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
