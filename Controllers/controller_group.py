from sqlalchemy.orm import Session

from Models import SessionLocal, Group


class GroupController:
    """Controller for Group-related actions"""

    def __init__(self, view, permissions, menu):
        self.view = view
        self.permissions = permissions
        self.menu = menu
        self.db: Session = SessionLocal()

    def create_group(self, group_name: str):
        new_group = Group(group_name=group_name)
        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return new_group

    def get_update_group_options(self, role_name):
        """Return update group options based on the user's role."""

        menu_options = {
            "Update Group Name": "Update_group_name",
            "Validate Change and return to group menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items()
                if self.permissions.has_permission(role_name, action)}

    def update_group(self, group, access_token):
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

        group = self.get_group(group)

        if group:
            self.db.delete(group)
            self.db.commit()
            return True

        return False

    def get_group(self, group_id: int):
        return self.db.query(Group).filter(Group.id == group_id).first()

    def handle_create_group(self, access_token):
        self.menu.token_check(access_token)

        group_name = self.view.prompt_for_name("group")
        self.create_group(group_name)
        self.view.display_message("created", "Group")

    def handle_update_group(self, group, access_token):
        self.menu.token_check(access_token)

        group = self.update_group(group)

        if group:
            self.view.display_message("updated", "Group")

        else:
            self.view.display_message("not found", "Group")

    def handle_get_group(self, access_token):
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
        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()
        if choice:
            success = self.delete_group(group)

            if success:
                self.view.display_message("deleted", "Group")

            else:
                self.view.display_message("not found", "Group")
