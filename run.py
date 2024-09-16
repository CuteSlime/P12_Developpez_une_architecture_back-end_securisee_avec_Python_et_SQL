import sentry

from Views import Views
from Controllers import Menu, Controller
from Models import Base, engine, SessionLocal
from permissions import PermissionManager


def main():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    view = Views()
    permissions = PermissionManager()
    menu = Menu(view, permissions, session)
    app = Controller(view, menu)

    app.run()


# sentry.run_sentry()
if __name__ == "__main__":
    main()
