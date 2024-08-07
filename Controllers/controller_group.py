from sqlalchemy.orm import Session
from Models import SessionLocal, Group


class GroupController:
    """Controller for Group-related actions"""

    def __init__(self, view):
        self.view = view
        self.db: Session = SessionLocal()

    def create_group(self, group_name: str):
        new_group = Group(group_name=group_name)
        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return new_group

    def update_group(self, group_id: int):
        group = self.get_group(group_id)
        if group:
            while True:
                match self.view.get_group_update_choice(group.group_name):
                    case "1":
                        group_name = self.view.prompt_for_name("group")
                        group.group_name = group_name
                    case "2":
                        break
            self.db.commit()
            self.db.refresh(group)
            return group
        return None

    def delete_group(self, group_id: int):
        group = self.get_group(group_id)
        if group:
            self.db.delete(group)
            self.db.commit()
            return True
        return False

    def get_group(self, group_id: int):
        return self.db.query(Group).filter(Group.id == group_id).first()

    def handle_create_group(self):
        group_name = self.view.prompt_for_name("group")
        self.create_group(group_name)
        self.view.display_message("created", "Group")

    def handle_update_group(self, access_token):
        groups = self.db.query(Group).all()
        group_id = int(self.view.display_item_list_choices(
            groups, "group_name", "group"))
        group = self.update_group(group_id)
        if group:
            self.view.display_message("updated", "Group")
        else:
            self.view.display_message("not found", "Group")

    def handle_get_group(self, access_token):
        groups = self.db.query(Group).all()
        group_id = int(self.view.display_item_list_choices(
            groups, "group_name", "group"))
        group = self.get_group(group_id)
        if group:
            self.view.display_group(group)
            self.handle_delete_group(group)
        else:
            self.view.display_message("not found", "Group")

    def handle_delete_group(self, group):
        choice = self.view.get_delete_menu_choice()
        if choice == "1":
            success = self.delete_group(group.id)
            if success:
                self.view.display_message("deleted", "Group")
            else:
                self.view.display_message("not found", "Group")
