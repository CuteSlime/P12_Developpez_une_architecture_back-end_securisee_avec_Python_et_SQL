from .controller_user import UserController


class Menu:
    def __init__(self, view):
        self.view = view
        self.user_controller = UserController(view)

    def main_menu(self):
        """Main menu"""
        choice = self.view.get_main_menu_choice()
        if choice == "1":
            self.user_controller.handle_create_user()
        if choice == "2":
            return exit()
