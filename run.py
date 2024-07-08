import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_user = os.environ.get('DB_USER')
db_pwd = os.environ.get('DB_PWD')
db_host = os.environ.get('DB_HOST', "localhost")
db_port = os.environ.get('DB_PORT', "3306")
db_name = os.environ.get('DB_NAME', "epic_events")


engine = create_engine(
    f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}')

try:
    connect = engine.connect()
    print("success!")
except Exception as ex:
    print(ex)
    # with Session(engine) as session:
    #     users = session.execute(select(User)).scalars().all()
