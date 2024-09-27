from datetime import datetime

import questionary


class Views:
    '''main view'''

    def __init__(self):
        self.custom_style = questionary.Style([
            ('qmark', 'fg:#E91E63 bold'),
            ('question', 'fg:#673AB7 bold'),
            ('answer', 'fg:#2196F3 bold'),
            ('pointer', 'fg:#673AB7 bold'),
            ('highlighted', 'fg:#03A9F4 bold'),
        ])

    def display_menu(self, available_menus, title):
        """Display a menu and return the user's choice."""

        return questionary.select(
            title,
            choices=available_menus,
        ).unsafe_ask()

    def get_delete_menu_choice(self):
        """ask the User to confirm delete"""

        return questionary.confirm("Did you really want to delete this?").unsafe_ask()

    def display_item_list_choices(self, items, attr_name, name):
        """Display a list of items for the user to choose from."""

        def get_nested_attr(item, attr_name):
            attrs = attr_name.split('.')

            for attr in attrs:
                item = getattr(item, attr, None)

                if item is None:
                    break

            return item

        if isinstance(attr_name, str):
            attr_name = [attr_name]

        choices = [
            questionary.Choice(
                title=" | ".join(
                    [str(get_nested_attr(item, attr) or "")
                     for attr in attr_name]
                ),
                value=item.id
            )
            for item in items
        ]

        choice = questionary.select(
            f"Choose {name}",
            choices=choices,
        ).unsafe_ask()
        return choice

    def prompt_for_name(self, name_of, *optional):
        """ask the user to input a name"""

        return (questionary.text(f"Enter {name_of} name{optional[0]}: ").unsafe_ask()
                if optional else questionary.text(f"Enter {name_of} name: ").unsafe_ask())

    def prompt_for_email(self):
        """ask the user to input an email"""

        return questionary.text("Enter email: ").unsafe_ask()

    def prompt_for_phone_number(self):
        """ask the user to input a phone number"""

        return questionary.text("Enter Customer phone number: ").unsafe_ask()

    def prompt_for_detail(self, detail_type, *optional):
        """ask the user to input some detail"""

        return (questionary.text(f"Enter any {detail_type} {optional[0]}: ").unsafe_ask()
                if optional else questionary.text(f"Enter any {detail_type}: ").unsafe_ask())

    def prompt_for_total_price(self):
        """ask the user to input a total price for the contract"""
        while True:
            total_price = questionary.text(
                "Enter the total price for the Customer.").unsafe_ask()
            try:
                total_price = float(total_price.replace(",", "."))
                break
            except ValueError:
                questionary.print("value error, please enter a valid number")
        return total_price

    def prompt_for_remaining_to_pay(self):
        """ask the user to input the remaining amount that the customer still have to pay"""
        while True:
            remaining_to_pay = questionary.text(
                "Enter the remaining amount to pay.").unsafe_ask()
            try:
                remaining_to_pay = float(remaining_to_pay.replace(",", "."))
                break
            except ValueError:
                questionary.print("value error, please enter a valid number")
        return remaining_to_pay

    def prompt_for_attendees(self):
        """ask the user to input the number of attendees"""
        while True:
            attendees = questionary.text(
                "Enter the number of attendees: ").unsafe_ask()

            try:
                int(attendees)
                break
            except ValueError:
                questionary.print("you should enter a number.")

        return attendees

    def prompt_for_password(self):
        """ask the user to input a password"""

        return questionary.password("Enter password: ").unsafe_ask()

    def date_input(self, start_or_end):
        """Receives a date from the user, validates it, and returns it in a specified format."""

        while True:
            try:
                user_input = questionary.text(
                    f"Enter the {start_or_end}"
                    + " date and time (e.g., 5 May 2023 @ 5PM or 05/05/2023 17H): ").unsafe_ask()

                try:
                    date = datetime.strptime(user_input, "%d %B %Y @ %I%p")

                except ValueError:
                    try:
                        date = datetime.strptime(
                            user_input, "%d/%m/%Y %HH%MMH")

                    except ValueError:
                        date = datetime.strptime(user_input, "%d/%m/%Y %HH")

                break

            except ValueError:
                questionary.print(
                    "Invalid format, examples of valid formats: 5 May 2023 @ 5PM or 05/05/2023 17H")

        return date

    def display_message(self, message_type, *model):
        """display the message correponding to the argument"""

        match message_type:
            case "created":
                questionary.print(f"{model[0]} created successfully!")

            case "updated":
                questionary.print(f"{model[0]} updated successfully!")

            case "deleted":
                questionary.print(f"{model[0]} deleted successfully!")

            case "not found":
                questionary.print(f"Error: {model[0]} not found!")

            case "expired token":
                questionary.print(
                    "\nSession expired, please log again.", style="bold red")

            case "invalid token":
                questionary.print("This token is not valid.")

            case "no customer":
                questionary.print(
                    "You don't have any customers.")

            case "no signed contract":
                questionary.print(
                    "no signed contract")

            case "no perms":
                questionary.print(
                    "you don't have the permission to access this.")

            case "signed":
                questionary.print("Contract has been signed.")

            case "not signed":
                questionary.print("Contract his not signed anymore.")

    def display_user(self, user):
        """display an user information"""

        questionary.print(" ___________________", style="bold green")
        questionary.print("| User ID: ", style="bold green", end='')
        questionary.print(f"{user.id}")
        questionary.print("| Full Name: ", style="bold green", end='')
        questionary.print(f"{user.full_name}")
        questionary.print("| Email: ", style="bold green", end='')
        questionary.print(f"{user.email}")
        questionary.print("| Group ID: ", style="bold green", end='')
        questionary.print(f"{user.group_id}")

    def display_group(self, group):
        """display a group information"""

        questionary.print(" ___________________", style="bold green")
        questionary.print("| Group ID: ", style="bold green", end='')
        questionary.print(f"{group.id}")
        questionary.print("| Group Name: ", style="bold green", end='')
        questionary.print(f"{group.group_name}")

    def display_customer(self, customer):
        """display a customer information"""

        questionary.print(" ___________________", style="bold green")
        questionary.print("| Customer ID: ", style="bold green", end='')
        questionary.print(f"{customer.id}")

        if customer.information:
            questionary.print("| Information: ", style="bold green", end='')
            questionary.print(f"{customer.information}")

        questionary.print("| Full Name: ", style="bold green", end='')
        questionary.print(f"{customer.full_name}")
        questionary.print("| Email: ", style="bold green", end='')
        questionary.print(f"{customer.email}")
        questionary.print("| Phone Number: ", style="bold green", end='')
        questionary.print(f"{customer.phone_number}")

        if customer.company_name:
            questionary.print("| Company name: ", style="bold green", end='')
            questionary.print(f"{customer.company_name}")

        questionary.print("| Sales representative: ",
                          style="bold green", end='')
        questionary.print(f"{customer.sales_representative.full_name}")

    def display_contract(self, contract):
        """display a contract information"""

        questionary.print(" ___________________", style="bold green")
        questionary.print("| Contract ID: ", style="bold green", end='')
        questionary.print(f"{contract.id}")
        questionary.print("| creation date: ", style="bold green", end='')
        questionary.print(f"{contract.contract_creation}")
        questionary.print("| Price of the Event: ",
                          style="bold green", end='')

        questionary.print(f"{contract.total_price}")
        questionary.print("| still needed to pay: ",
                          style="bold green", end='')

        questionary.print(f"{contract.remaining_to_pay}")
        questionary.print("| signed: ", style="bold green", end='')
        questionary.print(f"{"yes" if contract.statut else "no"}")
        questionary.print("Customer data:", style="bold lightgreen", end='')
        self.display_customer(contract.customer_data)

    def display_event(self, event):
        """display an event information"""

        questionary.print(" ___________________", style="bold green")
        questionary.print("| Event ID: ", style="bold green", end='')
        questionary.print(f"{event.id}")
        questionary.print("| Contract ID: ", style="bold green", end='')
        questionary.print(f"{event.contract_id}")
        questionary.print("| Customer name: ", style="bold green", end='')
        questionary.print(f"{event.customer_data.full_name}")
        questionary.print("| Customer contact: ", style="bold green", end='')
        questionary.print(f"{event.customer_data.email}")
        questionary.print("|                   ", style="bold green", end='')
        questionary.print(f"{event.customer_data.phone_number}")
        questionary.print("| Event date start: ", style="bold green", end='')
        questionary.print(f"{event.event_start}")
        questionary.print("| Event date end: ", style="bold green", end='')
        questionary.print(f"{event.event_end}")
        questionary.print("| Support: ", style="bold green", end='')
        questionary.print(f"{event.support.full_name}")
        questionary.print("| Location: ", style="bold green", end='')
        questionary.print(f"{event.location}")
        questionary.print("| attendees: ", style="bold green", end='')
        questionary.print(f"{event.attendees}")
        questionary.print("| notes: ", style="bold green", end='')
        questionary.print(f"{event.notes}")

    def login(self, retry=False):
        """menu principal

        Returns:
            _tulpe_: user login information
        """
        if retry:
            questionary.print("\n"
                              "|Sorry,\n"
                              "|Your username or password didn't match any accounts\n"
                              "|Please try again\n",
                              style="bold fg:red"
                              )

        else:
            questionary.print("\n"
                              "|Hello,\n"
                              "|Welcome into EpicEvents CRM.\n"
                              "|Please login\n",
                              style="bold fg:yellow"
                              )

        username = questionary.text('Username:').unsafe_ask()
        password = questionary.password("Password:").unsafe_ask()

        return (username, password)
