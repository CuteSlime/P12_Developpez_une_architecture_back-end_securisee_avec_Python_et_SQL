from Views import Views
from Controllers import Menu, Controller
from Models import Base, engine


def main():
    Base.metadata.create_all(bind=engine)

    view = Views()
    menu = Menu(view)
    app = Controller(view, menu)

    try:
        app.run()
    finally:
        app.close()


if __name__ == "__main__":
    main()
