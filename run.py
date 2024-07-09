from Views.view import Views
from Controllers.controller_menu import Menu
from Controllers.controller import Controller


def main():
    view = Views()
    menu = Menu(view)
    logiciel = Controller(view, menu)
    logiciel.run()


if __name__ == "__main__":
    main()
