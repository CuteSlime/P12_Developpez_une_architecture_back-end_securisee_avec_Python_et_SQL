from .controller_user import UserController


class Menu:
    def __init__(self, view):
        self.view = view
        self.user_controller = UserController(view)

    def main_menu(self):
        """Main menu"""
        choice = self.view.get_main_menu_choice()
        if choice == "1":
            self.user_menu()
        elif choice == "2":
            return exit()

    def user_menu(self):
        while True:
            choice = self.view.get_model_menu_choice('User')
            if choice == "1":
                self.user_controller.handle_create_user()
            elif choice == "2":
                self.user_controller.handle_update_user()
            elif choice == "3":
                self.user_controller.handle_get_user()
            elif choice == "4":
                return

