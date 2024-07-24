from sqlalchemy.orm import Session
from Models import SessionLocal, User, Group


class UserController:
    """Controller for User-related actions"""

    def __init__(self, view):
        self.view = view
        self.db: Session = SessionLocal()

    def create_user(self, full_name: str, email: str, password: str, group_id: int):
        new_user = User(full_name=full_name, email=email, group_id=group_id)
        new_user.set_password(password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            while True:
                choice = self.view.get_user_update_choice(user.full_name)
                if choice == "1":
                    full_name = self.view.prompt_for_name("full")
                    user.full_name = full_name
                elif choice == "2":
                    email = self.view.prompt_for_email()
                    user.email = email
                elif choice == "3":
                    password = self.view.prompt_for_password()
                    user.set_password(password)
                elif choice == "4":
                    groups = self.db.query(Group).all()
                    group_id = int(self.view.display_item_list_choices(
                        groups, "group_name", "group"))
                    user.group_id = group_id
                elif choice == "5":
                    break
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def handle_create_user(self):
        full_name = self.view.prompt_for_name("full")
        email = self.view.prompt_for_email()
        password = self.view.prompt_for_password()
        groups = self.db.query(Group).all()
        group_id = int(self.view.display_item_list_choices(
            groups, "group_name", "group"))
        self.create_user(full_name, email, password, group_id)
        self.view.display_success_message("User created successfully!")

    def handle_update_user(self):
        users = self.db.query(User).all()
        user_id = int(self.view.display_item_list_choices(
            users, "full_name", "user"))
        user = self.update_user(user_id)
        if user:
            self.view.display_success_message("User updated successfully!")
        else:
            self.view.display_error_message("User not found!")

    def handle_get_user(self):
        users = self.db.query(User).all()
        user_id = int(self.view.display_item_list_choices(
            users, "full_name", "user"))
        user = self.get_user(user_id)
        if user:
            self.view.display_user(user)
            self.handle_delete_user(user)
        else:
            self.view.display_error_message("User not found!")

    def handle_delete_user(self, user):
        choice = self.view.get_delete_menu_choice()
        if choice == "1":
            success = self.delete_user(user.id)
            if success:
                self.view.display_success_message("User deleted successfully!")
            else:
                self.view.display_error_message("User not found!")
