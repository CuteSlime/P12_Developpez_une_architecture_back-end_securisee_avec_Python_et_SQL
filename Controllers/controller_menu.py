from sqlalchemy.orm import Session
from Models import SessionLocal, User, Group

from .controller_user import UserController
from .controller_group import GroupController
from .controller_customer import CustomerController
from .controller_contract import ContractController
from .controller_event import EventController


class Menu:
    def __init__(self, view, permissions):
        self.view = view
        self.db: Session = SessionLocal()
        self.permissions = permissions
        self.user_controller = UserController(view, permissions, menu=self)
        self.group_controller = GroupController(view, permissions, menu=self)
        self.customer_controller = CustomerController(
            view, permissions, menu=self)
        self.contract_controller = ContractController(
            view, permissions, menu=self)
        self.event_controller = EventController(view, permissions, menu=self)

    def login(self, retry=False):
        """login menu"""

        while True:
            username, password = self.view.login(retry)
            try:
                user = self.db.query(User).filter(
                    User.full_name == username).first()
                if user and user.check_password(password):
                    print("success!")
                    access_token = User.create_access_token(
                        data={"username": user.full_name, "role": user.role.group_name})
                    # print(User.decode_access_token(access_token)["role"])
                    break
                else:
                    retry = True

            except Exception:
                retry = True
        self.main_menu(access_token)

    def token_check(self, access_token):
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            self.view.display_message("expired token")
            return self.login()
        elif verified_token is None:
            self.view.display_message("invalid token")
            return self.login()
        return verified_token["role"]

    def main_menu(self, access_token):
        """Main menu"""
        role_name = self.token_check(access_token)

        while True:
            menu_options = self.get_main_menu_options(role_name)
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit":
                return exit()

            getattr(self, menu_options[choice])(access_token)

    def user_menu(self, access_token):
        role_name = self.token_check(access_token)

        while True:
            menu_options = self.get_create_or_read_menu_options(
                role_name, "user")
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit to Main Menu":
                return

            getattr(self.user_controller, menu_options[choice])(access_token)

    def group_menu(self, access_token):
        role_name = self.token_check(access_token)

        while True:
            menu_options = self.get_create_or_read_menu_options(
                role_name, "group")
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit to Main Menu":
                return

            getattr(self.group_controller, menu_options[choice])(access_token)

    def customer_menu(self, access_token):
        role_name = self.token_check(access_token)

        while True:
            menu_options = self.get_create_or_read_menu_options(
                role_name, "customer")
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit to Main Menu":
                return

            getattr(self.customer_controller,
                    menu_options[choice])(access_token)

    def contract_menu(self, access_token):
        role_name = self.token_check(access_token)

        while True:
            menu_options = self.get_create_or_read_menu_options(
                role_name, "contract")
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit to Main Menu":
                return

            getattr(self.contract_controller,
                    menu_options[choice])(access_token)

    def event_menu(self, access_token):
        role_name = self.token_check(access_token)

        while True:
            menu_options = self.get_create_or_read_menu_options(
                role_name, "event")
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit to Main Menu":
                return

            getattr(self.event_controller, menu_options[choice])(access_token)

    def get_main_menu_options(self, role_name):
        """Return main menu options based on the user's role."""
        menu_options = {
            "Users Management": "user_menu",
            "Groups Management": "group_menu",
            "Customers Management": "customer_menu",
            "Contracts Management": "contract_menu",
            "Events Management": "event_menu",
            "Exit": "Exit"
        }
        return {option: action for option, action in menu_options.items() if self.permissions.has_permission(role_name, action)}

    def get_create_or_read_menu_options(self, role_name, model):
        """Return create or read menu options based on the user's role."""
        menu_options = {
            f"Create {model}": f"handle_create_{model}",
            f"Get {model}": f"handle_get_{model}",
            "Exit to Main Menu": "Exit"
        }

        return {option: action for option, action in menu_options.items() if self.permissions.has_permission(role_name, action)}

    def get_update_or_delete_menu_options(self, role_name, model):
        """Return update or delete menu options based on the user's role."""
        menu_options = {
            f"Update {model}": f"handle_update_{model}",
            f"Delete {model}": f"handle_delete_{model}",
            "Exit to Main Menu": "Exit"
        }

        return {option: action for option, action in menu_options.items() if self.permissions.has_permission(role_name, action)}
