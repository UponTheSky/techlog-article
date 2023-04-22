from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from ..config import config


engine = create_async_engine(url=config.DB_URL)
session_factory = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
