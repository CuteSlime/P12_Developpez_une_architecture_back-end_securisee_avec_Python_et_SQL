import sentry

from Views import Views
from Controllers import Menu, Controller
from Models import Base, Group, User, engine, SessionLocal
from permissions import PermissionManager


def main():
    """initialize the app with a database, session, view, permission, menu and the app itself before running the app"""

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    view = Views()
    permissions = PermissionManager()
    menu = Menu(view, permissions, session)
    app = Controller(view, menu)

    # create manager, commercial and support group
    if not session.query(Group).filter(Group.group_name == "Support").first():
        Support = Group(id=1, group_name="Support")
        session.add(Support)

    if not session.query(Group).filter(Group.group_name == "Management").first():
        Management = Group(id=2, group_name="Management")
        session.add(Management)

    if not session.query(Group).filter(Group.group_name == "Commercial").first():
        Commercial = Group(id=3, group_name="Commercial")
        session.add(Commercial)

    # if User DB empty (new DB) then create an admin account
    if session.query(User).count() == 0:
        admin = User(full_name="Admin", email="no_mail", group_id=2)
        admin.set_password("Admin")
        session.add(admin)

    session.commit()

    app.run()


sentry.run_sentry()
if __name__ == "__main__":
    main()
