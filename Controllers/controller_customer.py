import re

from sqlalchemy import func

from Models import Customer, User, Group


class CustomerController:
    """Controller for Customer-related actions"""

    def __init__(self, view, permissions, session, menu):
        """Initialize the CustomerController.

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

    def create_customer(self, information: str, full_name: str, email: str,
                        phone_number: str, company_name: str, user_id: int):
        """Create a new customer and add it to the database.

        Keyword arguments:
        information -- some information about the customer
        full_name -- the name of the customer
        email -- the name of the customer
        phone_number -- the name of the customer
        company_name -- the name of the customer
        user_id -- the ID of commercial linked to this customer

        Return: the created customer
        """

        new_customer = Customer(information=information, full_name=full_name, email=email,
                                phone_number=phone_number, company_name=company_name, user_id=user_id)
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def get_update_customer_options(self, role_name):
        """Return update customer options based on the user's role.

        Keyword arguments:
        role_name -- the name of the user's role
        Return: a dictionary of update options mapped to action names
        """

        menu_options = {
            "Update Information": "Update_customer_information",
            "Update Full Name": "Update_customer_fullname",
            "Update Email": "Update_customer_email",
            "Update Phone number": "Update_customer_phone_number",
            "Update Company name": "Update_customer_company_name",
            "Update Sales representative": "Update_customer_commercial",
            "Validate Change and return to customer menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items()
                if self.permissions.has_permission(role_name, action)}

    def update_customer(self, customer, access_token):
        """Update a customer's information based on input from the view.

        Keyword arguments:
        customer -- the customer to update
        access_token -- the access token for verifying user permissions
        Return: the updated customer, or None if no changes were made
        """

        role_name = self.menu.token_check(access_token)

        if customer:
            while True:
                title = "What did you want to edit from this customer?"
                menu_options = self.get_update_customer_options(role_name)
                choice = self.view.display_menu(
                    list(menu_options.keys()), title)

                match choice:
                    case "Update Information":
                        information = self.view.prompt_for_detail(
                            "information", "(can be empty)")
                        customer.information = information

                    case "Update Full Name":
                        full_name = self.view.prompt_for_name("customer")
                        customer.full_name = full_name

                    case "Update Email":
                        email = self.view.prompt_for_email()
                        customer.email = email

                    case "Update Phone number":
                        while True:
                            phone_number = self.view.prompt_for_phone_number()
                            phone_number = re.sub(r'\D', '', phone_number)
                            if len(phone_number) == 10:
                                break

                        customer.phone_number = phone_number

                    case "Update Company name":
                        company_name = self.view.prompt_for_name(
                            "company", "(can be empty)")
                        customer.company_name = company_name

                    case "Update Sales representative":
                        users = self.db.query(User).filter(User.group_id == 3)
                        user_id = int(self.view.display_item_list_choices(
                            users, "full_name", "user"))
                        customer.user_id = user_id

                    case "Validate Change and return to customer menu":
                        customer.last_update = func.now()
                        break

            self.db.commit()
            self.db.refresh(customer)
            return customer

        return None

    def delete_customer(self, customer):
        """Delete a customer from the database.

        Keyword arguments:
        customer -- the customer  to delete
        Return: True if the customer was deleted successfully, False otherwise
        """

        customer = self.get_customer(customer)

        if customer:
            self.db.delete(customer)
            self.db.commit()
            return True

        return False

    def get_customer(self, customer_id: int):
        """Retrieve a customer from the database by their ID.

        Keyword arguments:
        group_id -- the ID of the customer to retrieve
        Return: the retrieved customer, or None if not found
        """

        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def handle_create_customer(self, access_token):
        """Handle the process of creating a new customer through user input.

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

        user_name = verified_token["username"]

        information = self.view.prompt_for_detail(
            "information", "(can be empty)")
        full_name = self.view.prompt_for_name("customer")
        email = self.view.prompt_for_email()

        while True:
            phone_number = self.view.prompt_for_phone_number()
            phone_number = re.sub(r'\D', '', phone_number)

            if len(phone_number) == 10:
                break

        company_name = self.view.prompt_for_name("company", "(can be empty)")

        try:
            group_id = self.db.query(Group).filter(
                Group.group_name == "Commercial").first().id

            user_id = self.db.query(User).filter(
                User.group_id == group_id, User.full_name == user_name).first().id
        except Exception as e:
            print(e)
            return self.menu.login()

        self.create_customer(information, full_name, email,
                             phone_number, company_name, user_id)
        self.view.display_message("created", "Customer")

    def handle_update_customer(self, customer, access_token):
        """Handle the process of updating a customer through user input.

        Keyword arguments:
        customer -- the customer to update
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

        if customer.user_id == user.id:
            customer = self.update_customer(customer, access_token)

            if customer:
                self.view.display_message("updated", "Customer")
            else:
                self.view.display_message("not found", "Customer")

        else:
            self.view.display_message("no perms")
            return

    def handle_get_customer(self, access_token):
        """Handle retrieving and displaying a customer's information.

        Keyword arguments:
        access_token -- the access token for verifying user permissions
        """

        role_name = self.menu.token_check(access_token)

        customers = self.db.query(Customer).all()
        if not customers:
            self.view.display_message("not found", "Customer")
            return

        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))
        customer = self.get_customer(customer_id)
        if customer:
            self.view.display_customer(customer)
            title = "What did you want to do with this customer?"
            menu_options = self.menu.get_update_or_delete_menu_options(
                role_name, "customer")
            choice = self.view.display_menu(list(menu_options.keys()), title)
            if choice == "Exit to customer Menu":
                return

            getattr(self, menu_options[choice])(customer, access_token)

        else:
            self.view.display_message("not found", "Customer")

    def handle_delete_customer(self, customer, access_token):
        """Handle the process of deleting a customer through user input.

        Keyword arguments:
        customer -- the customer to delete
        access_token -- the access token for verifying user permissions
        """
        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()
        if choice:
            success = self.delete_customer(customer)
            if success:
                self.view.display_message("deleted", "Customer")
            else:
                self.view.display_message("not found", "Customer")
