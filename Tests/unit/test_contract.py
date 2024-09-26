from unittest.mock import patch

from Models import User, Contract, Customer


def test_contract_create(app, session):
    """test of handle_create and create function for contract

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """
    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")
    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=1)
    session.add(user)
    session.add(customer)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # Mock questionary and display_message
    with patch('questionary.text') as mock_text, \
            patch('questionary.select') as mock_select, \
            patch('questionary.print'), \
            patch.object(app.menu.contract_controller.view, 'display_message') as mock_display:

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "34", "12"
        ]
        mock_select.return_value.unsafe_ask.side_effect = [
            "1"
        ]

        app.menu.contract_controller.handle_create_contract(access_token)

        dummy_contract = session.query(Contract).filter_by(
            id=1).first()

        assert dummy_contract is not None, "The Dummy was not created in the DB"

        assert mock_text.call_count == 2, f"""questionary.text called {
            mock_text.call_count}/2"""
        assert mock_select.call_count == 1, f"""{
            mock_select.call_count}/1 customer selected"""
        assert mock_display.call_count == 1, f"""{
            mock_display.call_count}/1 creation message send"""


def test_contract_get(app, session):
    """test of handle_get and get function for contract

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """

    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")
    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=1)

    contract = Contract(customer_id=1, total_price=50,
                        remaining_to_pay=0, statut=False)

    session.add(user)
    session.add(customer)
    session.add(contract)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary and the handle_update/delete
    with patch('questionary.select') as mock_select, \
            patch('questionary.print'), \
            patch.object(app.menu.contract_controller, 'handle_update_contract') as mock_handle_update_contract:

        # mock selecting the menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "All contracts", "1", "Update contract",
            "contracts still unpaid",
            "contracts unsigned", "1", "Update contract",
            "All contracts", "1", "Exit to contract Menu"
        ]

        for _ in range(4):

            app.menu.contract_controller.handle_get_contract(access_token)

        assert mock_handle_update_contract.call_count == 2, f"""contract update was called {
            mock_handle_update_contract.call_count}/2"""

        assert mock_select.call_count == 10, f"""{
            mock_select.call_count}/10 menu tested"""


def test_contract_update(app, session):
    """test of handle_update and update function for contract

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """

    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")
    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=1)
    customer2 = Customer(information="information", full_name="Dummy2",
                         email="Dummy2@custom.com", phone_number="0987654321",
                         company_name="Dummy2 corp", user_id=1)

    contract = Contract(customer_id=1, total_price=50,
                        remaining_to_pay=50, statut=False)

    session.add(user)
    session.add(customer)
    session.add(customer2)
    session.add(contract)
    session.commit()

    test_user = session.query(User).filter_by(full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary
    with patch('questionary.text') as mock_text, \
            patch('questionary.select') as mock_select, \
            patch('questionary.print'):

        dummy_contract = session.query(
            Contract).filter_by(id=1).first()

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            34, 12
        ]

        mock_select.return_value.unsafe_ask.side_effect = [
            "Update customer", "2", "Update total price", "Update remaining to pay",
            "Update statut", "Validate Change and return to contract menu"
        ]

        app.menu.contract_controller.handle_update_contract(
            dummy_contract, access_token)

        assert dummy_contract.customer_id == 2, "contract customer is not Dummy2"
        assert dummy_contract.total_price == 34, "contract total_price is not 34"
        assert dummy_contract.remaining_to_pay == 12, "contract remaining_to_pay is not 12"
        assert dummy_contract.statut is True, "contract statut is unsigned"

        assert mock_text.call_count == 2, f"questionary.text called {
            mock_text.call_count}/2"

        assert mock_select.call_count == 6, f"""{
            mock_select.call_count}/6 menu tested"""

        # assert mock_display.call_count == 1, f"""{
        #     mock_display.call_count}/1 creation message send"""
