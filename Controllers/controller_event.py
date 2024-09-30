from datetime import datetime

from sqlalchemy import null, true

from Models import Event, Contract, Customer, User


class EventController:
    """Controller for Event-related actions"""

    def __init__(self, view, permissions, session, menu):
        """Initialize the EventController.

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

    def create_event(self, contract_id: int, customer_id: int, event_start: datetime,
                     event_end: datetime, location: str, attendees: int, notes: str):
        """Create a new event and add it to the database.

        Keyword arguments:
        contract_id -- the Contract ID linked to this event
        customer_id -- the customer ID linked to this event
        event_start -- start date for this event
        event_end -- end date for this event
        location -- location of the event
        attendees -- number of attendee for the event
        notes -- note aboout this event

        Return: the created event
        """

        new_event = Event(contract_id=contract_id, customer_id=customer_id,
                          event_start=event_start, event_end=event_end,
                          location=location, attendees=attendees, notes=notes)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return new_event

    def get_update_event_options(self, role_name):
        """Return update event options based on the user's role.

        Keyword arguments:
        role_name -- the name of the user's role
        Return: a dictionary of update options mapped to action names
        """

        menu_options = {
            "Update Contract": "Update_event_contract",
            "Update Customer": "Update_event_customer",
            "Update Event start date": "Update_event_start",
            "Update Event end date": "Update_event_end",
            "Update Support": "Update_event_support",
            "Update location": "Update_event_location",
            "Update number of atendees": "Update_event_atendees",
            "Update Notes": "Update_event_notes",
            "Validate Change and return to event Menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items()
                if self.permissions.has_permission(role_name, action)}

    def update_event(self, event, access_token):
        """Update a event's information based on input from the view.

        Keyword arguments:
        event -- the event to update
        access_token -- the access token for verifying user permissions
        Return: the updated event, or None if no changes were made
        """

        role_name = self.menu.token_check(access_token)

        if event:
            while True:
                title = "What did you want to edit from this event?"
                menu_options = self.get_update_event_options(role_name)
                choice = self.view.display_menu(
                    list(menu_options.keys()), title)

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
                        event.attendees = attendees

                    case "Update Notes":
                        notes = self.view.prompt_for_detail("notes")
                        event.notes = notes

                    case "Validate Change and return to event Menu":
                        break

            self.db.commit()
            self.db.refresh(event)
            return event

        return None

    def delete_event(self, event):
        """Delete a event from the database.

        Keyword arguments:
        event -- the event  to delete
        Return: True if the event was deleted successfully, False otherwise
        """

        if event:
            self.db.delete(event)
            self.db.commit()
            return True

        return False

    def get_event(self, event_id: int):
        """Retrieve a event from the database by their ID.

        Keyword arguments:
        group_id -- the ID of the event to retrieve
        Return: the retrieved event, or None if not found
        """

        return self.db.query(Event).filter(Event.id == event_id).first()

    def handle_create_event(self, access_token):
        """Handle the process of creating a new event through user input.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)
        verified_token = User.decode_access_token(access_token)

        if verified_token == "expired":
            self.view.display_message("expired token")
            return self.login()

        elif verified_token is None:
            self.view.display_message("invalid token")
            return self.login()

        username = verified_token["username"]

        user = self.db.query(User).filter(
            User.full_name == username).first()

        customers = self.db.query(Customer).filter(
            Customer.user_id == user.id).all()
        if not customers:
            self.view.display_message(
                "no customer", "You don't have any customers.")
            return

        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))

        contracts = self.db.query(Contract).filter(
            Contract.customer_id.in_([customer.id for customer in customers]),
            Contract.statut.is_(true())
        ).all()

        if not contracts:
            self.view.display_message(
                "no signed contract", "no signed contract")
            return

        contract_id = int(self.view.display_item_list_choices(
            contracts, "id", "contract"))

        event_start = self.view.date_input("event start")
        event_end = self.view.date_input("event end")

        location = self.view.prompt_for_detail("location")
        attendees = self.view.prompt_for_attendees()
        notes = self.view.prompt_for_detail("notes")
        self.create_event(contract_id, customer_id,
                          event_start, event_end, location, attendees, notes)

        self.view.display_message("created", "Event")

    def handle_update_event(self, event, access_token):
        """Handle the process of updating a event through user input.

        Keyword arguments:
        event -- the event to update
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)
        verified_token = User.decode_access_token(access_token)

        if verified_token == "expired":
            self.view.display_message("expired token")
            return self.login()

        elif verified_token is None:
            self.view.display_message("invalid token")
            return self.login()

        username = verified_token["username"]
        user = self.db.query(User).filter(
            User.full_name == username).first()

        if event.user_id == user.id:
            event = self.update_event(event, access_token)

            if event:
                self.view.display_message("updated", "Event")

            else:
                self.view.display_message("not found", "Event")

        else:
            self.view.display_message("no perms")
            return

    def get_event_filters(self, role_name):
        """Provide filtering options for events.

        Keyword arguments:
        role_name -- the name of the user's role
        Return: a dictionary of filter options mapped to action names
        """
        filter_options = {
            "All Events": "no_filter",
            "Events Without Support": "event_filter_no_support",
            "Events that you manage": "event_filter_is_support",
        }
        return {option: action for option, action in filter_options.items()
                if self.permissions.has_permission(role_name, action)}

    def handle_get_event(self, access_token):
        """Handle retrieving and displaying a event's information.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        role_name = self.menu.token_check(access_token)
        verified_token = User.decode_access_token(access_token)

        if verified_token == "expired":
            self.view.display_message("expired token")
            return self.login()

        elif verified_token is None:
            self.view.display_message("invalid token")
            return self.login()

        username = verified_token["username"]
        user = self.db.query(User).filter(
            User.full_name == username).first()

        filter_options = self.get_event_filters(role_name)
        title = "How would you like to filter the events?"
        filter_choice = self.view.display_menu(
            list(filter_options.keys()), title)

        filter_option = filter_options[filter_choice]
        events_query = self.db.query(Event)

        if filter_option == "event_filter_no_support":
            events_query = events_query.filter(Event.user_id.is_(null()))

        elif filter_option == "event_filter_is_support":
            events_query = events_query.filter(Event.user_id == user.id)

        events = events_query.all()

        if not events:
            self.view.display_message("not found", "Events")
            return

        event_id = int(self.view.display_item_list_choices(
            events, ["id", "contract.id", "customer_data.full_name"], "event"))
        event = self.get_event(event_id)

        if event:
            self.view.display_event(event)
            title = "What did you want to do with this event?"
            menu_options = self.menu.get_update_or_delete_menu_options(
                role_name, "event")

            choice = self.view.display_menu(list(menu_options.keys()), title)

            if choice == "Exit to event Menu":
                return

            getattr(self, menu_options[choice])(event, access_token)

        else:
            self.view.display_message("not found", "Event")

    def handle_delete_event(self, event, access_token):
        """Handle the process of deleting a event through user input.

        Keyword arguments:
        event -- the event to delete
        access_token -- the access token for verifying user permissions
        """

        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()
        if choice:
            success = self.delete_event(event)

            if success:
                self.view.display_message("deleted", "Event")

            else:
                self.view.display_message("not found", "Event")
