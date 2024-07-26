from getpass import getpass


class Views:
    '''main view'''

    def get_main_menu_choice(self):
        print("___________________")
        print("\n1. Users Management")
        print("2. Groups Management")
        print("3. Customers Management")
        print("4. Contracts Management")
        print("5. Exit")
        return input("Choose an option: ")

    def get_model_menu_choice(self, name):
        print("___________________")
        print(f"\n1. Create {name}")
        print(f"2. Update {name}")
        print(f"3. Get {name}")
        print("4. Exit to Main Menu")
        return input("Choose an option: ")

    def get_delete_menu_choice(self):
        print("___________________")
        print("\n1. Delete")
        print("2. Exit to Previous Menu")
        return input("Choose an option: ")

    def display_item_list_choices(self, items, attr_name, name):
        print("___________________\n")

        def get_nested_attr(item, attr_name):
            attrs = attr_name.split('.')
            for attr in attrs:
                item = getattr(item, attr)
            return item

        for item in items:
            print(f"{getattr(item, 'id')}. {get_nested_attr(item, attr_name)}")
        return input(f"Choose {name} by ID: ")

    def get_group_update_choice(self, name):
        print("___________________")
        print(f"\nWhat did you want to edit from Group {name} ?")
        print("1. Update Group Name")
        print("2. Validate Change and return to User Menu")
        return input("Choose an option: ")

    def get_user_update_choice(self, name):
        print("___________________")
        print(f"\nWhat did you want to edit from User {name} ?")
        print("1. Update Full Name")
        print("2. Update Email")
        print("3. Update Password")
        print("4. Update Group")
        print("5. Validate Change and return to User Menu")
        return input("Choose an option: ")

    def get_customer_update_choice(self, name):
        print("___________________")
        print(f"\nWhat did you want to edit from Customer {name} ?")
        print("1. Update Information")
        print("2. Update Full Name")
        print("3. Update Email")
        print("4. Update Phone number")
        print("5. Update Company name")
        print("6. Update Sales representative")
        print("7. Validate Change and return to User Menu")
        return input("Choose an option: ")

    def get_contract_update_choice(self):
        print("___________________")
        print(f"\nWhat did you want to edit from this Contract ?")
        print("1. Update customer")
        print("2. Update total_price")
        print("3. Update remaining_to_pay")
        print("4. Update statut")
        print("5. Validate Change and return to User Menu")
        return input("Choose an option: ")

    def prompt_for_name(self, name_of, *optional):
        return input(f"Enter {name_of} name{optional}: ")

    def prompt_for_email(self):
        return input("Enter email: ")

    def prompt_for_phone_number(self):
        return input("Enter Customer phone number: ")

    def prompt_for_detail(self, detail_type, *optional):
        return input(f"Enter any {detail_type} {optional}: ")

    def prompt_for_total_price(self):
        return input("Enter the total price for the Customer.")

    def prompt_for_remaining_to_pay(self):
        return input("Enter the remaining amount to pay.")

    def prompt_for_password(self):
        return getpass("Enter password: ")

    def display_message(self, message_type, *model):
        match message_type:
            case "created":
                print(f"{model[0]} created successfully!")
            case "updated":
                print(f"{model[0]} updated successfully!")
            case "deleted":
                print(f"{model[0]} deleted successfully!")
            case "not found":
                print(f"Error: {model[0]} not found!")
            case "signed":
                print("Contract has been signed.")
            case "not signed":
                print("Contract his not signed anymore.")

    def display_user(self, user):
        print(f"User ID: {user.id}, Full Name: {user.full_name}, Email: {
              user.email}, Group ID: {user.group_id}")

    def display_group(self, group):
        print(f"Group ID: {group.id}, Group Name: {group.group_name}")

    def display_customer(self, customer):
        print("  _____\n",
              f"| Customer ID: {customer.id}\n",
              f"{f"| Information: {customer.information}\n"
                 if customer.information else ""}"
              f"| Full Name: {customer.full_name}\n",
              f"| Email: {customer.email}\n",
              f"| Phone Number: {customer.phone_number}\n",
              f"{f"| Company name: {customer.company_name}\n"
                 if customer.company_name else ""}"
              f"| Sales representative: {customer.sales_representative.full_name}\n")

    def display_contract(self, contract):
        print("  _____\n",
              f"| Contract ID: {contract.id}\n",
              f"| creation date: {contract.contract_creation}\n",
              f"| Price of the Event: {contract.total_price}\n",
              f"| still needed to pay: {contract.remaining_to_pay}\n",
              f"| signed: {"yes" if contract.statut else "no"}\n",
              "Customer data:")
        self.display_customer(contract.customer_data)

    def main_menu(self, retry=False):
        '''menu principal

        Returns:
            _tulpe_: user login information
        '''
        if retry:
            print("\n"
                  "|Sorry,\n"
                  "|Your username or password didn't match any accounts\n"
                  "|Please try again\n"
                  )
            username = input('\nUsername:')
            password = getpass()
            return (username, password)
        else:
            print("\n"
                  "|Hello,\n"
                  "|Welcome into EpicEvents CRM.\n"
                  "|Please login\n"
                  )
            username = input('\nUsername:')
            password = getpass()
            return (username, password)
