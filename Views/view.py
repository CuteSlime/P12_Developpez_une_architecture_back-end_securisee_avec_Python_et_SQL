from getpass import getpass


class Views:
    '''main view'''

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
