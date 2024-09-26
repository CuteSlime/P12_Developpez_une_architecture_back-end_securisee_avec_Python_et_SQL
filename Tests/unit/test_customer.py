from unittest.mock import patch

from Models import User, Customer


def test_customer_create(app, session):
    """test of handle_create and create function for customer

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """
    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # Mock questionary and display_message
    with patch('questionary.text') as mock_text, \
            patch('questionary.print'), \
            patch.object(app.menu.customer_controller.view, 'display_message') as mock_display:

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "New information", "NewDummy", "Dummy@customer.com",
            "1234567890", "Dummy&co"
        ]
        app.menu.customer_controller.handle_create_customer(access_token)

        dummy_customer = session.query(Customer).filter_by(
            full_name="NewDummy").first()

        assert dummy_customer is not None, "The Dummy was not created in the DB"

        assert mock_text.call_count == 5, f"questionary.text called {
            mock_text.call_count}/5"
        assert mock_display.call_count == 1, f"""{
            mock_display.call_count}/1 creation message send"""


def test_customer_get(app, session):
    """test of handle_get and get function for customer

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

    # mock questionary and the handle_update/delete
    with patch('questionary.select') as mock_select, \
            patch('questionary.print'), \
            patch.object(app.menu.customer_controller, 'handle_update_customer') as mock_handle_update_customer:

        # mock selecting the menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "1", "Update customer", "1", "Exit to customer Menu"
        ]

        for _ in range(2):

            app.menu.customer_controller.handle_get_customer(access_token)

        assert mock_handle_update_customer.call_count == 1, f"""customer update was called {
            mock_handle_update_customer.call_count}/1"""

        assert mock_select.call_count == 4, f"""{
            mock_select.call_count}/4 menu tested"""


def test_customer_update(app, session):
    """test of handle_update and update function for customer

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")
    user2 = User(full_name="Seller", email="test@test.com", group_id=2)
    user2.set_password("test_password")
    customer = Customer(information="information", full_name="Dummy",
                        email="Dummy@custom.com", phone_number="0987654321",
                        company_name="Dummy corp", user_id=1)

    session.add(user)
    session.add(user2)
    session.add(customer)
    session.commit()

    test_user = session.query(User).filter_by(full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary
    with patch('questionary.text') as mock_text, \
            patch('questionary.select') as mock_select, \
            patch('questionary.print'):

        dummy = session.query(Customer).filter_by(full_name="Dummy").first()

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "New information", "NewDummy", "Dummy@customer.com",
            "1234567890", "Dummy&co"
        ]

        mock_select.return_value.unsafe_ask.side_effect = [
            "Update Information", "Update Full Name", "Update Email",
            "Update Phone number", "Update Company name", "Update Sales representative", "2",
            "Validate Change and return to customer menu"
        ]

        app.menu.customer_controller.handle_update_customer(
            dummy, access_token)

        assert dummy.information == "New information", "customer information is not New information"
        assert dummy.full_name == "NewDummy", "customer full_name is not NewDummy"
        assert dummy.email == "Dummy@customer.com", "customer email is not Dummy@customer.com"
        assert dummy.phone_number == "1234567890", "customer phone_number is not 1234567890"
        assert dummy.company_name == "Dummy&co", "customer company_name is not Dummy&co"
        assert dummy.user_id == 2, "customer is not atributed to user 2"

        assert mock_text.call_count == 5, f"questionary.text called {
            mock_text.call_count}/5"

        assert mock_select.call_count == 8, f"""{
            mock_select.call_count}/8 menu tested"""
