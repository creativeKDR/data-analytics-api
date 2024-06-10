import pyodbc
from fabricAir_api.src.core import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

pyodbc.pooling = False

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_size=30, pool_recycle=1800, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# decorator for session handle
def get_db_session(func):
    def wrapper(*args, **kwargs):
        session = scoped_session(SessionLocal)
        try:
            return func(*args, **kwargs, db=session)
        except Exception as e:
            print(str(e))
        finally:
            session.close()

    return wrapper
