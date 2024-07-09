import os


from sqlalchemy import create_engine


class Menu:
    def __init__(self, view):
        self.view = view

    def main_menu(self):
        """Main menu"""

        username, password = self.view.main_menu()
        need_retry = True
        while need_retry:
            db_user = username
            db_pwd = password
            db_host = os.environ.get('DB_HOST', "localhost")
            db_port = os.environ.get('DB_PORT', "3306")
            db_name = os.environ.get('DB_NAME', "epic_events")

            engine = create_engine(
                f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}')
            try:
                connect = engine.connect()
                print("success!")
                need_retry = False
            except Exception:
                username, password = self.view.main_menu(need_retry)

            # if username == "Admin" and password == "test":
            #     print("good")
            #     need_retry = False
            # else:
            #     print("bad")
            #     username, password = self.view.main_menu(need_retry)
        os.system('pause')
        exit()


# db_user = username
# db_pwd = password
# db_host = os.environ.get('DB_HOST', "localhost")
# db_port = os.environ.get('DB_PORT', "3306")
# db_name = os.environ.get('DB_NAME', "epic_events")


# engine = create_engine(
#     f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}')

# try:
#     connect = engine.connect()
#     print("success!")
# except Exception as ex:
#     print(ex)
# with Session(engine) as session:
#     users = session.execute(select(User)).scalars().all()
