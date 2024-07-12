from getpass import getpass


class Views:
    '''main view'''

    def get_main_menu_choice(self):
        print("1. Create User")
        print("2. Exit")
        return input("Choose an option: ")

    def prompt_for_full_name(self):
        return input("Enter full name: ")

    def prompt_for_email(self):
        return input("Enter email: ")

    def prompt_for_password(self):
        return input("Enter password: ")

    def display_success_message(self, message):
        print(message)

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
