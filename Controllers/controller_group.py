from Models import Group


class GroupController:
    """Controller for Group-related actions"""

    def __init__(self, view, permissions, session, menu):
        """Initialize the GroupController.

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

    def create_group(self, group_name: str):
        """Create a new group and add it to the database.

        Keyword arguments:
        group_name -- the name of the group

        Return: the created group
        """

        new_group = Group(group_name=group_name)
        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return new_group

    def get_update_group_options(self, role_name):
        """Return update group options based on the user's role.

        Keyword arguments:
        role_name -- the name of the user's role
        Return: a dictionary of update options mapped to action names
        """

        menu_options = {
            "Update Group Name": "Update_group_name",
            "Validate Change and return to group menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items()
                if self.permissions.has_permission(role_name, action)}

    def update_group(self, group, access_token):
        """Update a group's information based on input from the view.

        Keyword arguments:
        group -- the group to update
        access_token -- the access token for verifying user permissions
        Return: the updated group, or None if no changes were made
        """

        role_name = self.menu.token_check(access_token)

        if group:
            while True:
                title = "What did you want to edit from this group?"
                menu_options = self.get_update_group_options(role_name)
                choice = self.view.display_menu(
                    list(menu_options.keys()), title)

                match choice:
                    case "Update Group Name":
                        group_name = self.view.prompt_for_name("group")
                        group.group_name = group_name

                    case "Validate Change and return to group menu":
                        break

            self.db.commit()
            self.db.refresh(group)
            return group

        return None

    def delete_group(self, group):
        """Delete a group from the database.

        Keyword arguments:
        group -- the group  to delete
        Return: True if the group was deleted successfully, False otherwise
        """

        group = self.get_group(group)

        if group:
            self.db.delete(group)
            self.db.commit()
            return True

        return False

    def get_group(self, group_id: int):
        """Retrieve a group from the database by their ID.

        Keyword arguments:
        group_id -- the ID of the group to retrieve
        Return: the retrieved group, or None if not found
        """

        return self.db.query(Group).filter(Group.id == group_id).first()

    def handle_create_group(self, access_token):
        """Handle the process of creating a new group through user input.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        group_name = self.view.prompt_for_name("group")
        self.create_group(group_name)
        self.view.display_message("created", "Group")

    def handle_update_group(self, group, access_token):
        """Handle the process of updating a group through user input.

        Keyword arguments:
        group -- the group to update
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        group = self.update_group(group)

        if group:
            self.view.display_message("updated", "Group")

        else:
            self.view.display_message("not found", "Group")

    def handle_get_group(self, access_token):
        """Handle retrieving and displaying a group's information.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        role_name = self.menu.token_check(access_token)

        groups = self.db.query(Group).all()
        group_id = int(self.view.display_item_list_choices(
            groups, "group_name", "group"))

        group = self.get_group(group_id)

        if group:
            self.view.display_user(group)
            title = "What did you want to do with this group?"
            menu_options = self.menu.get_update_or_delete_menu_options(
                role_name, "group")

            choice = self.view.display_menu(list(menu_options.keys()), title)

            if choice == "Exit to Main Menu":
                return

            getattr(self, menu_options[choice])(group, access_token)

        else:
            self.view.display_message("not found", "Group")

    def handle_delete_group(self, group, access_token):
        """Handle the process of deleting a group through user input.

        Keyword arguments:
        group -- the group to delete
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()
        if choice:
            success = self.delete_group(group)

            if success:
                self.view.display_message("deleted", "Group")

            else:
                self.view.display_message("not found", "Group")
