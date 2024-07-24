from .controller_user import UserController
from .controller_group import GroupController
from .controller_customer import CustomerController


class Menu:
    def __init__(self, view):
        self.view = view
        self.user_controller = UserController(view)
        self.group_controller = GroupController(view)
        self.customer_controller = CustomerController(view)

    def main_menu(self):
        """Main menu"""
        match self.view.get_main_menu_choice():
            case "1":
                self.user_menu()
            case "2":
                self.group_menu()
            case "3":
                self.customer_menu()
            case "4":
                return exit()

    def user_menu(self):
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

    def group_menu(self):
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

    def customer_menu(self):
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
