from sqlalchemy.orm import Session
from Models import SessionLocal, User


class UserController:
    """Controller for User-related actions"""

    def __init__(self, view):
        self.view = view
        self.db: Session = SessionLocal()

    def create_user(self, full_name: str, email: str, password: str):
        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def handle_create_user(self):
        full_name = self.view.prompt_for_full_name()
        email = self.view.prompt_for_email()
        password = self.view.prompt_for_password()
        self.create_user(full_name, email, password)
        self.view.display_success_message("User created successfully!")

    def close(self):
        self.db.close()
