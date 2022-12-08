from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_NAME = 'fapi'
DB_HOST = 'localhost'
DB_PASS = ''
DB_UNAME = 'vsh'
DB_PORT = 5432
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_UNAME}:''@{DB_HOST}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base