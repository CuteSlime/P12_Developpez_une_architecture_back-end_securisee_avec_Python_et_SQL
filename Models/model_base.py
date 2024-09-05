import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()
db_user = os.environ.get('DB_USER', "username")
db_pwd = os.environ.get('DB_PWD', "password")
db_host = os.environ.get('DB_HOST', "localhost")
db_port = os.environ.get('DB_PORT', "3306")
db_name = os.environ.get('DB_NAME', "epic_events2")

DATABASE_URL = f'mysql+pymysql://{db_user}:{
    db_pwd}@{db_host}:{db_port}/{db_name}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
