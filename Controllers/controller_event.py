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

    def update_event(self, event_id: int):
        event = self.get_event(event_id)
        if event:
            while True:
                match self.view.get_event_update_choice():
                    case "1":
                        print("1. Update Contract")
                        contracts = self.db.query(Contract).all()
                        contract_id = int(self.view.display_item_list_choices(
                            contracts, "contract.id", "contract"))
                        event.contract_id = contract_id
                    case "2":
                        print("2. Update Customer")
                        customers = self.db.query(Customer).all()
                        customer_id = int(self.view.display_item_list_choices(
                            customers, "customer_data.full_name", "customer"))
                        event.customer_id = customer_id
                    case "3":
                        print("3. Update Event start date")
                        event_start = self.view.date_input("event start")
                        event.event_start = event_start
                    case "4":
                        print("4. Update Event end date")
                        event_end = self.view.date_input("event end")
                        event.event_end = event_end
                    case "5":
                        print("5. Update Support")
                        users = self.db.query(User).all()
                        user_id = int(self.view.display_item_list_choices(
                            users, "support.full_name", "user"))
                        event.user_id = user_id
                    case "6":
                        print("6. Update location")
                        location = self.view.prompt_for_detail("location")
                        event.location = location
                    case "7":
                        print("7. Update number of atendees")
                        attendees = self.view.prompt_for_attendees()
                        attendees = int(attendees)
                        event.attendees = attendees
                    case "8":
                        print("8. Update Notes")
                        notes = self.view.prompt_for_detail("notes")
                        event.notes = notes
                    case "9":
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

    def handle_create_event(self):
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
        events = self.db.query(Event).all()
        event_id = int(self.view.display_item_list_choices(
            events, "contract.id", "event"))
        event = self.update_event(event_id)
        if event:
            self.view.display_message("updated", "Event")
        else:
            self.view.display_message("not found", "Event")

    def handle_get_event(self, access_token):
        events = self.db.query(Event).all()
        event_id = int(self.view.display_item_list_choices(
            events, "contract.id", "event"))
        event = self.get_event(event_id)
        if event:
            self.view.display_event(event)
            self.handle_delete_event(event)
        else:
            self.view.display_message("not found", "Event")

    def handle_delete_event(self, event):
        choice = self.view.get_delete_menu_choice()
        if choice == "1":
            success = self.delete_event(event.id)
            if success:
                self.view.display_message("deleted", "Event")
            else:
                self.view.display_message("not found", "Event")
