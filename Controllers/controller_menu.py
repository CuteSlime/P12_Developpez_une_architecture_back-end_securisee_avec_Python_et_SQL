from sqlalchemy.orm import Session
from Models import SessionLocal, User, Group

from .controller_user import UserController
from .controller_group import GroupController
from .controller_customer import CustomerController
from .controller_contract import ContractController
from .controller_event import EventController


class Menu:
    def __init__(self, view):
        self.view = view
        self.db: Session = SessionLocal()
        self.user_controller = UserController(view)
        self.group_controller = GroupController(view)
        self.customer_controller = CustomerController(view)
        self.contract_controller = ContractController(view)
        self.event_controller = EventController(view)

    def login(self):
        """login menu"""

        username, password = self.view.login()
        while True:
            try:
                user = self.db.query(User).filter(
                    User.full_name == username).first()
                if user and user.check_password(password):
                    print("success!")
                    access_token = User.create_access_token(
                        data={"username": user.full_name, "role": user.role.group_name})
                    # print(User.decode_access_token(access_token)["role"])

            except Exception as e:
                print(e)
                username, password = self.view.login(True)

            break

        self.main_menu(access_token)

    def main_menu(self, access_token):
        """Main menu"""
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            return self.login()
        role_name = verified_token["role"]

        while True:
            match self.view.get_main_menu_choice():
                case "1":
                    if role_name in ("Management"):
                        self.user_menu(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.main_menu(access_token)
                case "2":
                    if role_name in ("Management"):
                        self.group_menu(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.main_menu(access_token)

                case "3":
                    if role_name in ("Commercial"):
                        self.customer_menu(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.main_menu(access_token)

                case "4":
                    if role_name in ("Management", "Commercial"):
                        self.contract_menu(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.main_menu(access_token)

                case "5":
                    if role_name in ("Support", "Management", "Commercial"):
                        self.event_menu(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.main_menu(access_token)

                case "6":
                    return exit()

    def user_menu(self, access_token):
        while True:
            match self.view.get_model_menu_choice('User'):
                case "1":
                    self.user_controller.handle_create_user()
                case "2":
                    self.user_controller.handle_update_user()
                case "3":
                    self.user_controller.handle_get_user()
                case "4":
                    return

    def group_menu(self, access_token):
        while True:
            match self.view.get_model_menu_choice('Group'):
                case "1":
                    self.group_controller.handle_create_group()
                case "2":
                    self.group_controller.handle_update_group()
                case "3":
                    self.group_controller.handle_get_group()
                case "4":
                    return

    def customer_menu(self, access_token):
        while True:
            match self.view.get_model_menu_choice('Customer'):
                case "1":
                    self.customer_controller.handle_create_customer()
                case "2":
                    self.customer_controller.handle_update_customer()
                case "3":
                    self.customer_controller.handle_get_customer()
                case "4":
                    return

    def contract_menu(self, access_token):
        while True:
            match self.view.get_model_menu_choice('Contract'):
                case "1":
                    self.contract_controller.handle_create_contract()
                case "2":
                    self.contract_controller.handle_update_contract()
                case "3":
                    self.contract_controller.handle_get_contract()
                case "4":
                    return

    def event_menu(self, access_token):
        while True:
            match self.view.get_model_menu_choice('Event'):
                case "1":
                    self.event_controller.handle_create_event()
                case "2":
                    self.event_controller.handle_update_event()
                case "3":
                    self.event_controller.handle_get_event()
                case "4":
                    return
