from getpass import getpass


class Views:
    '''main view'''

    def get_main_menu_choice(self):
        print("___________________")
        print("\n1. User Management")
        print("2. Group Management")
        print("3. Exit")
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
        for item in items:
            print(f"{getattr(item, 'id')}. {getattr(item, attr_name)}")
        return input(f"Choose {name} by ID: ")

    def get_user_update_choice(self, name):
        print("___________________")
        print(f"\nWhat did you want to edit from User {name} ?")
        print("1. Update Full Name")
        print("2. Update Email")
        print("3. Update Password")
        print("4. Update Group")
        print("5. Validate Change and return to User Menu")
        return input("Choose an option: ")

    def get_group_update_choice(self, name):
        print("___________________")
        print(f"\nWhat did you want to edit from Group {name} ?")
        print("1. Update Group Name")
        print("2. Validate Change and return to User Menu")
        return input("Choose an option: ")

    def prompt_for_full_name(self):
        return input("Enter full name: ")

    def prompt_for_email(self):
        return input("Enter email: ")

    def prompt_for_password(self):
        return getpass("Enter password: ")

    def prompt_for_group_name(self):
        return input("Enter group name: ")

    def display_success_message(self, message):
        print(message)

    def display_error_message(self, message):
        print(f"Error: {message}")

    def display_user(self, user):
        print(f"User ID: {user.id}, Full Name: {user.full_name}, Email: {
              user.email}, Group ID: {user.group_id}")

    def display_group(self, group):
        print(f"Group ID: {group.id}, Group Name: {group.group_name}")

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
