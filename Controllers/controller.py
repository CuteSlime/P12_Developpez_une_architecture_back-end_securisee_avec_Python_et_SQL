
class Controller:
    """Main controller"""

    def __init__(self, view, menu):

        self.view = view
        self.menu = menu

    def run(self):

        while True:
            self.menu.main_menu()

    def close(self):
        self.menu.close()
