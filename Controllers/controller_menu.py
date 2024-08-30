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
        self.customer_controller = CustomerController(view, menu=self)
        self.contract_controller = ContractController(view)
        self.event_controller = EventController(view)

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
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            return self.login()
        role_name = verified_token["role"]
        while True:
            match self.view.get_model_menu_choice('User'):
                case "1":
                    if role_name in ("Management"):
                        self.user_controller.handle_create_user()
                    else:
                        self.view.display_message("no perms")
                        self.user_menu(access_token)
                case "2":
                    if role_name in ("Management"):
                        self.user_controller.handle_update_user(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.user_menu(access_token)
                case "3":
                    if role_name in ("Management"):
                        self.user_controller.handle_get_user(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.user_menu(access_token)
                case "4":
                    return

    def group_menu(self, access_token):
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            return self.login()
        role_name = verified_token["role"]
        while True:
            match self.view.get_model_menu_choice('Group'):
                case "1":
                    if role_name in ("Management"):
                        self.group_controller.handle_create_group()
                    else:
                        self.view.display_message("no perms")
                        self.group_menu(access_token)
                case "2":
                    if role_name in ("Management"):
                        self.group_controller.handle_update_group(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.group_menu(access_token)
                case "3":
                    if role_name in ("Management"):
                        self.group_controller.handle_get_group(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.group_menu(access_token)
                case "4":
                    return

    def customer_menu(self, access_token):
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            return self.login()
        role_name = verified_token["role"]
        while True:
            match self.view.get_model_menu_choice('Customer'):
                case "1":
                    if role_name in ("Commercial"):
                        self.customer_controller.handle_create_customer(
                            access_token)
                    else:
                        self.view.display_message("no perms")
                        self.customer_menu(access_token)
                case "2":
                    if role_name in ("Commercial"):
                        self.customer_controller.handle_update_customer(
                            access_token)
                    else:
                        self.view.display_message("no perms")
                        self.customer_menu(access_token)
                case "3":
                    if role_name in ("Support", "Management", "Commercial"):
                        self.customer_controller.handle_get_customer(
                            access_token)
                    else:
                        self.view.display_message("no perms")
                        self.customer_menu(access_token)
                case "4":
                    return

    def contract_menu(self, access_token):
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            return self.login()
        role_name = verified_token["role"]
        while True:
            match self.view.get_model_menu_choice('Contract'):
                case "1":
                    if role_name in ("Management"):
                        self.contract_controller.handle_create_contract()
                    else:
                        self.view.display_message("no perms")
                        self.contract_menu(access_token)
                case "2":
                    if role_name in ("Management", "Commercial"):
                        self.contract_controller.handle_update_contract(
                            access_token)
                    else:
                        self.view.display_message("no perms")
                        self.contract_menu(access_token)
                case "3":
                    if role_name in ("Support", "Management", "Commercial"):
                        self.contract_controller.handle_get_contract(
                            access_token)
                    else:
                        self.view.display_message("no perms")
                        self.contract_menu(access_token)
                case "4":
                    return

    def event_menu(self, access_token):
        verified_token = User.decode_access_token(access_token)
        if verified_token == "expired":
            return self.login()
        print(verified_token)
        role_name = verified_token["role"]
        while True:
            match self.view.get_model_menu_choice('Event'):
                case "1":
                    if role_name in ("Commercial"):
                        self.event_controller.handle_create_event()
                    else:
                        self.view.display_message("no perms")
                        self.event_menu(access_token)
                case "2":
                    if role_name in ("Support", "Management"):
                        self.event_controller.handle_update_event(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.event_menu(access_token)
                case "3":
                    if role_name in ("Support", "Management", "Commercial"):
                        self.event_controller.handle_get_event(access_token)
                    else:
                        self.view.display_message("no perms")
                        self.event_menu(access_token)
                case "4":
                    return
