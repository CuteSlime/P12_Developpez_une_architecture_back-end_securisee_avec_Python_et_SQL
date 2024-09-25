from sqlalchemy.orm import Session

from Models import SessionLocal, Contract, Customer, User


class ContractController:
    """Controller for Contract-related actions"""

    def __init__(self, view, permissions, session, menu):
        self.view = view
        self.permissions = permissions
        self.menu = menu
        self.db = session

    def create_contract(self, customer_id: int, total_price: float, remaining_to_pay: float):
        new_contract = Contract(
            customer_id=customer_id, total_price=total_price, remaining_to_pay=remaining_to_pay)
        self.db.add(new_contract)
        self.db.commit()
        self.db.refresh(new_contract)
        return new_contract

    def get_update_contract_options(self, role_name):
        """Return update contract options based on the user's role."""

        menu_options = {
            "Update customer": "Update_contract_customer",
            "Update total price": "Update_contract_total_price",
            "Update remaining to pay": "Update_contract_remaining_to_pay",
            "Update statut": "Update_contract_statut",
            "Validate Change and return to contract menu": "Validate_Change",
        }
        return {option: action for option, action in menu_options.items()
                if self.permissions.has_permission(role_name, action)}

    def update_contract(self, contract, access_token):
        role_name = self.menu.token_check(access_token)

        if contract:
            while True:
                title = "What did you want to edit from this contract?"
                menu_options = self.get_update_contract_options(role_name)
                choice = self.view.display_menu(
                    list(menu_options.keys()), title)

                match choice:
                    case "Update customer":
                        customers = self.db.query(Customer).all()
                        customer_id = int(self.view.display_item_list_choices(
                            customers, "full_name", "customer"))
                        contract.customer_id = customer_id

                    case "Update total price":
                        total_price = self.view.prompt_for_total_price()
                        contract.total_price = total_price

                    case "Update remaining to pay":
                        remaining_to_pay = self.view.prompt_for_remaining_to_pay()
                        contract.remaining_to_pay = remaining_to_pay

                    case "Update statut":
                        contract.statut = not contract.statut

                        if contract.statut:
                            self.view.display_message("signed")

                        else:
                            self.view.display_message("not signed")

                    case "Validate Change and return to contract menu":
                        break

            self.db.commit()
            self.db.refresh(contract)
            return contract

        return None

    def delete_contract(self, contract):

        contract = self.get_contract(contract)

        if contract:
            self.db.delete(contract)
            self.db.commit()
            return True

        return False

    def get_contract(self, contract_id: int):
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def handle_create_contract(self, access_token):
        self.menu.token_check(access_token)

        customers = self.db.query(Customer).all()
        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))
        total_price = self.view.prompt_for_total_price()
        total_price = float(total_price.replace(",", "."))
        remaining_to_pay = self.view.prompt_for_remaining_to_pay()
        remaining_to_pay = float(remaining_to_pay.replace(",", "."))
        self.create_contract(customer_id, total_price, remaining_to_pay)
        self.view.display_message("created", "Contract")

    def handle_update_contract(self, contract, access_token):
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
        customer = self.db.query(Customer).filter(
            Customer.id == contract.customer_id).first()

        if customer.user_id == user.id:
            contract = self.update_contract(contract, access_token)

            if contract:
                self.view.display_message("updated", "Contract")

            else:
                self.view.display_message("not found", "Contract")

        else:
            self.view.display_message("no perms")
            return

    def get_contract_filters(self, role_name):
        """Provide filtering options for contracts."""

        filter_options = {
            "All contracts": "no_filter",
            "contracts unsigned": "contract_filter_unsigned",
            "contracts still unpaid": "contract_filter_unpaid",
        }
        return {option: action for option, action in filter_options.items()
                if self.permissions.has_permission(role_name, action)}

    def handle_get_contract(self, access_token):
        role_name = self.menu.token_check(access_token)

        filter_options = self.get_contract_filters(role_name)
        title = "How would you like to filter the contracts?"
        filter_choice = self.view.display_menu(
            list(filter_options.keys()), title)
        filter_option = filter_options[filter_choice]
        contracts_query = self.db.query(Contract)

        if filter_option == "contract_filter_unpaid":
            contracts_query = contracts_query.filter(
                Contract.remaining_to_pay > 0)

        elif filter_option == "contract_filter_unsigned":
            contracts_query = contracts_query.filter(Contract.statut is False)

        contracts = contracts_query.all()

        if not contracts:
            self.view.display_message("not found", "Contracts")
            return

        contract_id = int(self.view.display_item_list_choices(
            contracts, "customer_data.full_name", "contract"))
        contract = self.get_contract(contract_id)

        if contract:
            self.view.display_contract(contract)
            title = "What did you want to do with this contract?"
            menu_options = self.menu.get_update_or_delete_menu_options(
                role_name, "contract")
            choice = self.view.display_menu(list(menu_options.keys()), title)

            if choice == "Exit to contract Menu":
                return

            getattr(self, menu_options[choice])(contract, access_token)

        else:
            self.view.display_message("not found", "Contract")

    def handle_delete_contract(self, contract, access_token):
        self.menu.token_check(access_token)

        choice = self.view.get_delete_menu_choice()

        if choice:
            success = self.delete_contract(contract)

            if success:
                self.view.display_message("deleted", "Contract")

            else:
                self.view.display_message("not found", "Contract")
