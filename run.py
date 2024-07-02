from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from Models import User

mysql_user = ""
mysql_pwd = ""
database = "epic_events"


engine = create_engine(
    f'mysql://{mysql_user}:{mysql_pwd}@localhost/{database}')

with Session(engine) as session:
    users = session.execute(select(User)).scalars().all()
