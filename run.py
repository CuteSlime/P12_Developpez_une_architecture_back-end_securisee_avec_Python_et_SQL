import sentry

from Views import Views
from Controllers import Menu, Controller
from Models import Base, engine
from permissions import PermissionManager


def main():
    Base.metadata.create_all(bind=engine)

    view = Views()
    permissions = PermissionManager()
    menu = Menu(view, permissions)
    app = Controller(view, menu)

    app.run()


# sentry.run_sentry()
if __name__ == "__main__":
    main()
