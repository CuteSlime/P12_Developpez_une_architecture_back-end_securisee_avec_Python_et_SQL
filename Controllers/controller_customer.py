import re

from sqlalchemy import func
from sqlalchemy.orm import Session

from Models import SessionLocal, Customer, User


class CustomerController:
    """Controller for Customer-related actions"""

    def __init__(self, view, permissions, session, menu):
        self.view = view
        self.permissions = permissions
        self.menu = menu
        self.db = session

    def create_customer(self, information: str, full_name: str, email: str,
                        phone_number: str, company_name: str, user_id: int):
        new_customer = Customer(information=information, full_name=full_name, email=email,
                                phone_number=phone_number, company_name=company_name, user_id=user_id)
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def get_update_customer_options(self, role_name):
        """Return update customer options based on the user's role."""

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

        customer = self.get_customer(customer)

        if customer:
            self.db.delete(customer)
            self.db.commit()
            return True

        return False

    def get_customer(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def handle_create_customer(self, access_token):
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
            user_id = self.db.query(User).filter(
                User.group_id == 3, User.full_name == user_name).first().id
        except Exception as e:
            print(e)
            return self.menu.login()

        self.create_customer(information, full_name, email,
                             phone_number, company_name, user_id)
        self.view.display_message("created", "Customer")

    def handle_update_customer(self, customer, access_token):
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
        role_name = self.menu.token_check(access_token)

        customers = self.db.query(Customer).all()
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
        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()
        if choice:
            success = self.delete_customer(customer)
            if success:
                self.view.display_message("deleted", "Customer")
            else:
                self.view.display_message("not found", "Customer")
