from getpass import getpass


class Views:
    '''main view'''

    def get_main_menu_choice(self):
        print("___________________")
        print("\n1. User Management")
        print("2. Group Management")
        print("3. Customer Management")
        print("4. Exit")
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

    def prompt_for_name(self, name_of, *optional):
        return input(f"Enter {name_of} name{optional}: ")

    def prompt_for_email(self):
        return input("Enter email: ")

    def prompt_for_phone_number(self):
        return input("Enter Customer phone number: ")

    def prompt_for_detail(self, detail_type, *optional):
        return input(f"Enter any {detail_type} {optional}: ")

    def prompt_for_password(self):
        return getpass("Enter password: ")

    def display_message(self, message_type, *model):
        match message_type:
            case "created":
                print(f"{model} created successfully!")
            case "updated":
                print(f"{model} updated successfully!")
            case "deleted":
                print(f"{model} deleted successfully!")
            case "not found":
                print(f"Error: {model} not found!")
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
        print(f""" Customer ID: {customer.id}, Information: {customer.information},
              Full Name: {customer.full_name}, Email: {customer.email},
              Phone Number: {customer.phone_number}, Company name: {customer.company_name},
              Sales representative: {customer.user_id}""")

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
