from Models import User, Group


class UserController:
    """Controller for User-related actions"""

    def __init__(self, view, permissions, session, menu):
        """Initialize the UserController.

        Keyword arguments:
        view -- the view responsible for displaying user interactions
        permissions -- the permissions used to check user permissions
        session -- the session for interacting with the database
        menu -- the menu for handling menu-related tasks
        """

        self.view = view
        self.permissions = permissions
        self.menu = menu
        self.db = session

    def create_user(self, full_name: str, email: str, password: str, group_id: int):
        """Create a new user and add it to the database.

        Keyword arguments:
        full_name -- the name of the user
        email -- the user's email address
        password -- the user's password
        group_id -- the ID of the group the user belongs to
        Return: the created user
        """
        new_user = User(full_name=full_name, email=email, group_id=group_id)
        new_user.set_password(password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_update_user_options(self, role_name):
        """Return update user options based on the user's role.

        Keyword arguments:
        role_name -- the name of the user's role
        Return: a dictionary of update options mapped to action names
        """

        menu_options = {
            "Update Full Name": "Update_user_fullname",
            "Update Email": "Update_user_email",
            "Update Password": "Update_user_password",
            "Update Group": "Update_user_group",
            "Validate Change and return to user menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items()
                if self.permissions.has_permission(role_name, action)}

    def update_user(self, user, access_token):
        """Update a user's information based on input from the view.

        Keyword arguments:
        user -- the user to update
        access_token -- the access token for verifying user permissions
        Return: the updated user, or None if no changes were made
        """

        role_name = self.menu.token_check(access_token)

        if user:
            while True:
                title = "What did you want to edit from this user?"
                menu_options = self.get_update_user_options(role_name)
                choice = self.view.display_menu(
                    list(menu_options.keys()), title)

                match choice:
                    case "Update Full Name":
                        full_name = self.view.prompt_for_name("full")
                        user.full_name = full_name

                    case "Update Email":
                        email = self.view.prompt_for_email()
                        user.email = email

                    case "Update Password":
                        password = self.view.prompt_for_password()
                        user.set_password(password)

                    case "Update Group":
                        groups = self.db.query(Group).all()
                        group_id = int(self.view.display_item_list_choices(
                            groups, "group_name", "group"))
                        user.group_id = group_id

                    case "Validate Change and return to user menu":
                        break

            self.db.commit()
            self.db.refresh(user)
            return user

        return None

    def delete_user(self, user):
        """Delete a user from the database.

        Keyword arguments:
        user -- the user  to delete
        Return: True if the user was deleted successfully, False otherwise
        """

        if user:
            self.db.delete(user)
            self.db.commit()
            return True

        return False

    def get_user(self, user_id: int):
        """Retrieve a user from the database by their ID.

        Keyword arguments:
        user_id -- the ID of the user to retrieve
        Return: the retrieved user, or None if not found
        """

        return self.db.query(User).filter(User.id == user_id).first()

    def handle_create_user(self, access_token):
        """Handle the process of creating a new user through user input.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        full_name = self.view.prompt_for_name("full")
        email = self.view.prompt_for_email()
        password = self.view.prompt_for_password()
        groups = self.db.query(Group).all()
        group_id = int(self.view.display_item_list_choices(
            groups, "group_name", "group"))

        self.create_user(full_name, email, password, group_id)
        self.view.display_message("created", "User")

    def handle_update_user(self, user, access_token):
        """Handle the process of updating a user through user input.

        Keyword arguments:
        user -- the user to update
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        user = self.update_user(user, access_token)

        if user:
            self.view.display_message("updated", "User")

        else:
            self.view.display_message("not found", "User")

    def handle_get_user(self, access_token):
        """Handle retrieving and displaying a user's information.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        role_name = self.menu.token_check(access_token)

        users = self.db.query(User).all()
        user_id = int(self.view.display_item_list_choices(
            users, "full_name", "user"))

        user = self.get_user(user_id)

        if user:
            self.view.display_user(user)
            title = "What did you want to do with this user?"
            menu_options = self.menu.get_update_or_delete_menu_options(
                role_name, "user")

            choice = self.view.display_menu(list(menu_options.keys()), title)

            if choice == "Exit to user Menu":
                return

            getattr(self, menu_options[choice])(user, access_token)

        else:
            self.view.display_message("not found", "User")

    def handle_delete_user(self, user, access_token):
        """Handle the process of deleting a user through user input.

        Keyword arguments:
        user -- the user to delete
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()

        if choice:
            success = self.delete_user(user)

            if success:
                self.view.display_message("deleted", "User")

            else:
                self.view.display_message("not found", "User")
