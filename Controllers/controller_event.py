from datetime import datetime

from sqlalchemy.orm import Session

from Models import SessionLocal, Event, Contract, Customer, User


class EventController:
    """Controller for Event-related actions"""

    def __init__(self, view, permissions, menu):
        self.view = view
        self.permissions = permissions
        self.menu = menu
        self.db: Session = SessionLocal()

    def create_event(self, contract_id: int, customer_id: int,
                     event_start: datetime, event_end: datetime,
                     user_id: int, location: str, attendees: int, notes: str):
        new_event = Event(contract_id=contract_id, customer_id=customer_id,
                          event_start=event_start, event_end=event_end,
                          user_id=user_id, location=location, attendees=attendees, notes=notes)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return new_event

    def get_update_event_options(self, role_name):
        """Return update event options based on the user's role."""

        menu_options = {
            "Update Contract": "Update_Contract",
            "Update Customer": "Update_Customer",
            "Update Event start date": "Update_Event_start",
            "Update Event end date": "Update_Event_end",
            "Update Support": "Update_Support",
            "Update location": "Update_location",
            "Update number of atendees": "Update_atendees",
            "Update Notes": "Update_Notes",
            "Validate Change and return to User Menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items() if self.permissions.has_permission(role_name, action)}

    def update_event(self, event_id: int, access_token):
        role_name = self.menu.token_check(access_token)

        event = self.get_event(event_id)
        if event:
            while True:
                menu_options = self.get_update_event_options(role_name)
                choice = self.view.display_menu(list(menu_options.keys()))

                match choice:
                    case "Update Contract":
                        contracts = self.db.query(Contract).all()
                        contract_id = int(self.view.display_item_list_choices(
                            contracts, "contract.id", "contract"))
                        event.contract_id = contract_id
                    case "Update Customer":
                        customers = self.db.query(Customer).all()
                        customer_id = int(self.view.display_item_list_choices(
                            customers, "customer_data.full_name", "customer"))
                        event.customer_id = customer_id
                    case "Update Event start date":
                        event_start = self.view.date_input("event start")
                        event.event_start = event_start
                    case "Update Event end date":
                        event_end = self.view.date_input("event end")
                        event.event_end = event_end
                    case "Update Support":
                        users = self.db.query(User).filter(User.group_id == 1)
                        user_id = int(self.view.display_item_list_choices(
                            users, "full_name", "user"))
                        event.user_id = user_id
                    case "Update location":
                        location = self.view.prompt_for_detail("location")
                        event.location = location
                    case "Update number of atendees":
                        attendees = self.view.prompt_for_attendees()
                        attendees = int(attendees)
                        event.attendees = attendees
                    case "Update Notes":
                        notes = self.view.prompt_for_detail("notes")
                        event.notes = notes
                    case "Validate Change and return to User Menu":
                        break
            self.db.commit()
            self.db.refresh(event)
            return event
        return None

    def delete_event(self, event_id: int):
        event = self.get_event(event_id)
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False

    def get_event(self, event_id: int):
        return self.db.query(Event).filter(Event.id == event_id).first()

    def handle_create_event(self, access_token):
        role_name = self.menu.token_check(access_token)

        contracts = self.db.query(Contract).all()
        contract_id = int(self.view.display_item_list_choices(
            contracts, "id", "contract"))
        customers = self.db.query(Customer).all()
        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))
        event_start = self.view.date_input("event start")
        event_end = self.view.date_input("event end")
        users = self.db.query(User).filter(User.group_id == 1)
        user_id = int(self.view.display_item_list_choices(
            users, "full_name", "user"))
        location = self.view.prompt_for_detail("location")
        attendees = self.view.prompt_for_attendees()
        attendees = int(attendees)
        notes = self.view.prompt_for_detail("notes")
        self.create_event(contract_id, customer_id,
                          event_start, event_end, user_id, location, attendees, notes)
        self.view.display_message("created", "Event")

    def handle_update_event(self, access_token):
        role_name = self.menu.token_check(access_token)

        events = self.db.query(Event).all()
        event_id = int(self.view.display_item_list_choices(
            events, "contract.id", "event"))
        event = self.update_event(event_id, access_token)
        if event:
            self.view.display_message("updated", "Event")
        else:
            self.view.display_message("not found", "Event")

    def handle_get_event(self, access_token):
        role_name = self.menu.token_check(access_token)

        events = self.db.query(Event).all()
        event_id = int(self.view.display_item_list_choices(
            events, "contract.id", "event"))
        event = self.get_event(event_id)
        if event:
            self.view.display_event(event)
            menu_options = self.menu.get_update_or_delete_menu_options(
                role_name, "event")
            choice = self.view.display_menu(list(menu_options.keys()))
            if choice == "Exit to Main Menu":
                return

            getattr(self, menu_options[choice])(access_token)

        else:
            self.view.display_message("not found", "Event")

    def handle_delete_event(self, event, access_token):
        role_name = self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()
        if choice:
            success = self.delete_event(event.id)
            if success:
                self.view.display_message("deleted", "Event")
            else:
                self.view.display_message("not found", "Event")
