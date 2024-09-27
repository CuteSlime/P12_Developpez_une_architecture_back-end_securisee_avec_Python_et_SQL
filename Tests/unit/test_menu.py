from unittest.mock import patch

from Models import User


def test_main_menu(app, session):
    """Test main menu when the user chooses each item."""

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary, menus and sys.exit
    with patch('questionary.select') as mock_select, \
            patch.object(app.menu, 'user_menu') as mock_user_menu, \
            patch.object(app.menu, 'customer_menu') as mock_customer_menu, \
            patch.object(app.menu, 'contract_menu') as mock_contract_menu, \
            patch.object(app.menu, 'event_menu') as mock_event_menu, \
            patch('sys.exit') as mock_exit:

        # mock selecting menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "Users Management", "Customers Management",
            "Contracts Management", "Events Management", "Exit"
        ]

        app.menu.main_menu(access_token)

        assert mock_user_menu.call_count == 1, "user menu was not called"
        assert mock_user_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_customer_menu.call_count == 1, "customer menu was not called"
        assert mock_customer_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_contract_menu.call_count == 1, "contract menu was not called"
        assert mock_contract_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_event_menu.call_count == 1, "event menu was not called"
        assert mock_event_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"


def test_user_menu(app, session):
    """Test user menu when the user chooses each item."""

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary and handle function
    with patch('questionary.select') as mock_select, \
            patch.object(app.menu.user_controller, 'handle_create_user') as mock_handle_create_user, \
            patch.object(app.menu.user_controller, 'handle_get_user') as mock_handle_get_user:

        # mock selecting the user menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "Create user", "Get user", "Exit to Main Menu"
        ]

        app.menu.user_menu(access_token)

        assert mock_handle_create_user.call_count == 1, "user menu was not called"
        assert mock_handle_create_user.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_handle_get_user.call_count == 1, "user menu was not called"
        assert mock_handle_get_user.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_select.call_count == 3, (
            "Menu didn't loop through all options or try to loop more than they are option"
        )


def test_customer_menu(app, session):
    """Test customer menu when the user chooses each item."""

    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary and handle function
    with patch('questionary.select') as mock_select, \
            patch.object(app.menu.customer_controller, 'handle_create_customer') as mock_handle_create_customer, \
            patch.object(app.menu.customer_controller, 'handle_get_customer') as mock_handle_get_customer:

        # mock selecting the customer menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "Create customer", "Get customer", "Exit to Main Menu"
        ]

        app.menu.customer_menu(access_token)

        assert mock_handle_create_customer.call_count == 1, "customer menu was not called"
        assert mock_handle_create_customer.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_handle_get_customer.call_count == 1, "customer menu was not called"
        assert mock_handle_get_customer.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_select.call_count == 3, (
            "Menu didn't loop through all options or try to loop more than they are option"
        )


def test_contract_menu(app, session):
    """Test contract menu when the user chooses each item."""

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary and handle function
    with patch('questionary.select') as mock_select, \
            patch.object(app.menu.contract_controller, 'handle_create_contract') as mock_handle_create_contract, \
            patch.object(app.menu.contract_controller, 'handle_get_contract') as mock_handle_get_contract:

        # mock selecting the contract menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "Create contract", "Get contract", "Exit to Main Menu"
        ]

        app.menu.contract_menu(access_token)

        assert mock_handle_create_contract.call_count == 1, "contract menu was not called"
        assert mock_handle_create_contract.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_handle_get_contract.call_count == 1, "contract menu was not called"
        assert mock_handle_get_contract.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_select.call_count == 3, (
            "Menu didn't loop through all options or try to loop more than they are option"
        )


def test_event_menu(app, session):
    """Test event menu when the user chooses each item."""

    user = User(full_name="test_user", email="test@test.com", group_id=2)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary and handle function
    with patch('questionary.select') as mock_select, \
            patch.object(app.menu.event_controller, 'handle_create_event') as mock_handle_create_event, \
            patch.object(app.menu.event_controller, 'handle_get_event') as mock_handle_get_event:

        # mock selecting the event menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "Create event", "Get event", "Exit to Main Menu"
        ]

        app.menu.event_menu(access_token)

        assert mock_handle_create_event.call_count == 1, "event menu was not called"
        assert mock_handle_create_event.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_handle_get_event.call_count == 1, "event menu was not called"
        assert mock_handle_get_event.call_args == (
            (access_token,),), "didn't have the access token as argument"

        assert mock_select.call_count == 3, (
            "Menu didn't loop through all options or try to loop more than they are option"
        )
