from dotenv import load_dotenv


class Controller:
    """Main controller"""

    def __init__(self, view, menu):

        self.view = view
        self.menu = menu

    def run(self):

        while True:
            load_dotenv()
            self.menu.main_menu()
