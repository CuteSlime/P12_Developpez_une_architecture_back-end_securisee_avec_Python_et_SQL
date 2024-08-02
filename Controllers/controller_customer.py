import re
from sqlalchemy import func
from sqlalchemy.orm import Session
from Models import SessionLocal, Customer, User


class CustomerController:
    """Controller for Customer-related actions"""

    def __init__(self, view):
        self.view = view
        self.db: Session = SessionLocal()

    def create_customer(self, information: str, full_name: str, email: str,
                        phone_number: str, company_name: str, user_id: int):
        new_customer = Customer(information=information, full_name=full_name, email=email,
                                phone_number=phone_number, company_name=company_name, user_id=user_id)
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def update_customer(self, customer_id: int):
        customer = self.get_customer(customer_id)
        if customer:
            while True:
                match self.view.get_customer_update_choice(
                        customer.full_name):
                    case "1":
                        information = self.view.prompt_for_detail(
                            "information", "(can be empty)")
                        customer.information = information
                    case "2":
                        full_name = self.view.prompt_for_name("customer")
                        customer.full_name = full_name
                    case "3":
                        email = self.view.prompt_for_email()
                        customer.email = email
                    case "4":
                        while True:
                            phone_number = self.view.prompt_for_phone_number()
                            phone_number = re.sub(r'\D', '', phone_number)
                            if len(phone_number) == 10:
                                break
                        customer.phone_number = phone_number
                    case "5":
                        company_name = self.view.prompt_for_name(
                            "company", "(can be empty)")
                        customer.company_name = company_name
                    case "6":
                        users = self.db.query(User).filter(User.group_id == 3)
                        user_id = int(self.view.display_item_list_choices(
                            users, "full_name", "user"))
                        customer.user_id = user_id
                    case "7":
                        customer.last_update = func.now()
                        break
            self.db.commit()
            self.db.refresh(customer)
            return customer
        return None

    def delete_customer(self, customer_id: int):
        customer = self.get_customer(customer_id)
        if customer:
            self.db.delete(customer)
            self.db.commit()
            return True
        return False

    def get_customer(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def handle_create_customer(self, access_token):
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
        users = self.db.query(User).filter(User.group_id == 3)
        user_id = int(self.view.display_item_list_choices(
            users, "full_name", "user"))
        self.create_customer(information, full_name, email,
                             phone_number, company_name, user_id)
        self.view.display_message("created", "Customer")

    def handle_update_customer(self, access_token):
        customers = self.db.query(Customer).all()
        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))
        customer = self.update_customer(customer_id)
        if customer:
            self.view.display_message("updated", "Customer")
        else:
            self.view.display_message("not found", "Customer")

    def handle_get_customer(self, access_token):
        customers = self.db.query(Customer).all()
        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))
        customer = self.get_customer(customer_id)
        if customer:
            self.view.display_customer(customer)
            self.handle_delete_customer(customer)
        else:
            self.view.display_message("not found", "Customer")

    def handle_delete_customer(self, customer):
        choice = self.view.get_delete_menu_choice()
        if choice == "1":
            success = self.delete_customer(customer.id)
            if success:
                self.view.display_message("deleted", "Customer")
            else:
                self.view.display_message("not found", "Customer")
