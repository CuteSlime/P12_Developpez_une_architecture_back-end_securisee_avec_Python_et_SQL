from sqlalchemy.orm import Session
from Models import SessionLocal, Contract, Customer


class ContractController:
    """Controller for Contract-related actions"""

    def __init__(self, view, permissions, menu):
        self.view = view
        self.permissions = permissions
        self.menu = menu
        self.db: Session = SessionLocal()

    def create_contract(self, customer_id: int, total_price: float, remaining_to_pay: float):
        new_contract = Contract(
            customer_id=customer_id, total_price=total_price, remaining_to_pay=remaining_to_pay)
        self.db.add(new_contract)
        self.db.commit()
        self.db.refresh(new_contract)
        return new_contract

    def update_contract(self, contract_id: int):
        contract = self.get_contract(contract_id)
        if contract:
            while True:
                match self.view.get_contract_update_choice():
                    case "1":
                        customers = self.db.query(Customer).all()
                        customer_id = int(self.view.display_item_list_choices(
                            customers, "full_name", "customer"))
                        contract.customer_id = customer_id
                    case "2":
                        total_price = self.view.prompt_for_total_price()
                        contract.total_price = total_price
                    case "3":
                        remaining_to_pay = self.view.prompt_for_remaining_to_pay()
                        contract.remaining_to_pay = remaining_to_pay
                    case "4":
                        contract.statut = not contract.statut
                        if contract.statut:
                            self.view.display_message("signed")
                        else:
                            self.view.display_message("not signed")
                    case "5":
                        break
            self.db.commit()
            self.db.refresh(contract)
            return contract
        return None

    def delete_contract(self, contract_id: int):
        contract = self.get_contract(contract_id)
        if contract:
            self.db.delete(contract)
            self.db.commit()
            return True
        return False

    def get_contract(self, contract_id: int):
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def handle_create_contract(self):
        customers = self.db.query(Customer).all()
        customer_id = int(self.view.display_item_list_choices(
            customers, "full_name", "customer"))
        total_price = self.view.prompt_for_total_price()
        total_price = float(total_price.replace(",", "."))
        remaining_to_pay = self.view.prompt_for_remaining_to_pay()
        remaining_to_pay = float(remaining_to_pay.replace(",", "."))
        self.create_contract(customer_id, total_price, remaining_to_pay)
        self.view.display_message("created", "Contract")

    def handle_update_contract(self, access_token):
        contracts = self.db.query(Contract).all()
        contract_id = int(self.view.display_item_list_choices(
            contracts, "customer_data.full_name", "contract"))
        contract = self.update_contract(contract_id)
        if contract:
            self.view.display_message("updated", "Contract")
        else:
            self.view.display_message("not found", "Contract")

    def handle_get_contract(self, access_token):
        contracts = self.db.query(Contract).all()
        contract_id = int(self.view.display_item_list_choices(
            contracts, "customer_data.full_name", "contract"))
        contract = self.get_contract(contract_id)
        if contract:
            self.view.display_contract(contract)
            self.handle_delete_contract(contract)
        else:
            self.view.display_message("not found", "Contract")

    def handle_delete_contract(self, contract):
        choice = self.view.get_delete_menu_choice()
        if choice == "1":
            success = self.delete_contract(contract.id)
            if success:
                self.view.display_message("deleted", "Contract")
            else:
                self.view.display_message("not found", "Contract")
