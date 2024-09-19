from unittest.mock import patch


def test_main_menu_exit(app):
    """Test main menu when the user chooses to exit."""

    access_token = "valid_token"

    # Mock token_check to return the management role, mock questionary and sys.exit
    with patch.object(app.menu, 'token_check', return_value="Management"), \
            patch('questionary.select') as mock_select, \
            patch('sys.exit') as mock_exit:

        # mock selecting the exit choice before calling the function to test
        mock_select.return_value.unsafe_ask.return_value = "Exit"
        app.menu.main_menu(access_token)

        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"


def test_main_menu_user_menu(app):
    """Test main menu when the user chooses 'Users Management'."""

    access_token = "valid_token"

    # Mock token_check to return the management role, mock questionary, user_menu and sys.exit
    with patch.object(app.menu, 'token_check', return_value="Management"), \
            patch('questionary.select') as mock_select, \
            patch.object(app.menu, 'user_menu') as mock_user_menu, \
            patch('sys.exit') as mock_exit:

        # mock selecting the user menu choice in the first loop and exit in the seconde one
        # before calling the function to test
        mock_select.return_value.unsafe_ask.side_effect = [
            "Users Management", "Exit"]

        app.menu.main_menu(access_token)

        assert mock_user_menu.call_count == 1, "user menu was not called"
        assert mock_user_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"
        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"


def test_main_menu_group_menu(app):
    """Test main menu when the user chooses 'Groups Management'."""

    access_token = "valid_token"

    # Mock token_check to return the management role, mock questionary, group_menu and sys.exit
    with patch.object(app.menu, 'token_check', return_value="Management"), \
            patch('questionary.select') as mock_select, \
            patch.object(app.menu, 'group_menu') as mock_group_menu, \
            patch('sys.exit') as mock_exit:

        # mock selecting the groups menu choice in the first loop and exit in the seconde one
        # before calling the function to test
        mock_select.return_value.unsafe_ask.side_effect = [
            "Groups Management", "Exit"]

        app.menu.main_menu(access_token)

        assert mock_group_menu.call_count == 1, "groups menu was not called"
        assert mock_group_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"
        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"


def test_main_menu_customer_menu(app):
    """Test main menu when the user chooses 'Customers Management'."""

    access_token = "valid_token"

    # Mock token_check to return the management role, mock questionary, customer_menu and sys.exit
    with patch.object(app.menu, 'token_check', return_value="Management"), \
            patch('questionary.select') as mock_select, \
            patch.object(app.menu, 'customer_menu') as mock_customer_menu, \
            patch('sys.exit') as mock_exit:

        # mock selecting the customer menu choice in the first loop and exit in the seconde one
        # before calling the function to test
        mock_select.return_value.unsafe_ask.side_effect = [
            "Customers Management", "Exit"]

        app.menu.main_menu(access_token)

        assert mock_customer_menu.call_count == 1, "customer menu was not called"
        assert mock_customer_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"
        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"


def test_main_menu_contract_menu(app):
    """Test main menu when the user chooses 'Contracts Management'."""

    access_token = "valid_token"

    # Mock token_check to return the management role, mock questionary, contract_menu and sys.exit
    with patch.object(app.menu, 'token_check', return_value="Management"), \
            patch('questionary.select') as mock_select, \
            patch.object(app.menu, 'contract_menu') as mock_contract_menu, \
            patch('sys.exit') as mock_exit:

        # mock selecting the contract menu choice in the first loop and exit in the seconde one
        # before calling the function to test
        mock_select.return_value.unsafe_ask.side_effect = [
            "Contracts Management", "Exit"]

        app.menu.main_menu(access_token)

        assert mock_contract_menu.call_count == 1, "contract menu was not called"
        assert mock_contract_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"
        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"


def test_main_menu_event_menu(app):
    """Test main menu when the user chooses 'Events Management'."""

    access_token = "valid_token"

    # Mock token_check to return the management role, mock questionary, event_menu and sys.exit
    with patch.object(app.menu, 'token_check', return_value="Management"), \
            patch('questionary.select') as mock_select, \
            patch.object(app.menu, 'event_menu') as mock_event_menu, \
            patch('sys.exit') as mock_exit:

        # mock selecting the event menu choice in the first loop and exit in the seconde one
        # before calling the function to test
        mock_select.return_value.unsafe_ask.side_effect = [
            "Events Management", "Exit"]

        app.menu.main_menu(access_token)

        assert mock_event_menu.call_count == 1, "event menu was not called"
        assert mock_event_menu.call_args == (
            (access_token,),), "didn't have the access token as argument"
        assert mock_exit.call_count == 1, "Exit was not called"
        assert mock_exit.call_args == ((0,),), "didn't have 0 as argument"
