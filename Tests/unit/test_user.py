from unittest.mock import patch

from Models import User


def test_user_create(app, session):
    """test of handle_create and create function for user

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
            patch('questionary.password') as mock_password, \
            patch('questionary.select') as mock_select, \
            patch.object(app.menu.user_controller.view, 'display_message') as mock_display:

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "The Dummy2", "Dummy@CRM.com"
        ]
        mock_password.return_value.unsafe_ask.side_effect = [
            "The Dummy"
        ]
        mock_select.return_value.unsafe_ask.side_effect = [
            "1"
        ]
        app.menu.user_controller.handle_create_user(access_token)

        dummy_user = session.query(User).filter_by(
            full_name="The Dummy2").first()

        assert dummy_user is not None, "The Dummy was not created in the DB"

        assert mock_text.call_count == 2, f"questionary.text called {
            mock_text.call_count}/2"
        assert mock_password.call_count == 1, f"{
            mock_password.call_count}/1 password entered"
        assert mock_select.call_count == 1, f"{
            mock_select.call_count}/1 group selected"
        assert mock_display.call_count == 1, f"{
            mock_display.call_count}/1 creation message send"


def test_user_get(app, session):
    """test of handle_get and get function for user

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary and the handle_update/delete
    with patch('questionary.select') as mock_select, \
            patch('questionary.print'), \
            patch.object(app.menu.user_controller, 'handle_update_user') as mock_handle_update_user, \
            patch.object(app.menu.user_controller, 'handle_delete_user') as mock_handle_delete_user:

        # mock selecting the menu choices
        mock_select.return_value.unsafe_ask.side_effect = [
            "1", "Update user", "1", "Delete user", "1", "Exit to user Menu"
        ]

        for _ in range(3):

            app.menu.user_controller.handle_get_user(access_token)

        assert mock_handle_update_user.call_count == 1, f"""user update was called {
            mock_handle_update_user.call_count}/1"""
        assert mock_handle_delete_user.call_count == 1, f"""user delete was called {
            mock_handle_delete_user.call_count}/1"""

        assert mock_select.call_count == 6, f"""{
            mock_select.call_count}/6 menu tested"""


def test_user_update(app, session):
    """test of handle_update and update function for user

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")
    user2 = User(full_name="user2", email="user2@test.com", group_id=3)
    user2.set_password("user2_password")

    session.add(user)
    session.add(user2)
    session.commit()

    test_user = session.query(User).filter_by(full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary
    with patch('questionary.text') as mock_text, \
            patch('questionary.password') as mock_password, \
            patch('questionary.select') as mock_select, \
            patch('questionary.print'):

        dummy = session.query(User).filter_by(full_name="user2").first()

        # mock selecting and filling the menu choices
        mock_text.return_value.unsafe_ask.side_effect = [
            "The Dummy2", "Dummy@CRM.com"
        ]
        mock_password.return_value.unsafe_ask.side_effect = [
            "The Dummy"
        ]
        mock_select.return_value.unsafe_ask.side_effect = [
            "Update Full Name", "Update Email", "Update Password",
            "Update Group", "2", "Validate Change and return to user menu"
        ]

        app.menu.user_controller.handle_update_user(dummy, access_token)

        assert dummy.full_name == "The Dummy2", "user name is not \"The Dummy2\""
        assert dummy.email == "Dummy@CRM.com", "user email is not Dummy@CRM.com"
        assert dummy.group_id == 2, "user is not in the group 2"
        assert dummy.check_password(
            "The Dummy"), "encrypted password didn't match"

        assert mock_text.call_count == 2, f"questionary.text called {
            mock_text.call_count}/2"
        assert mock_password.call_count == 1, f"{
            mock_password.call_count}/1 password entered"

        assert mock_select.call_count == 6, f"""{
            mock_select.call_count}/6 menu tested"""


def test_user_delete(app, session):
    """test of handle_delete and delete function for user

    Keyword arguments:
    app -- the testing app run
    session: the session used for the testing DB
    """

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")
    user2 = User(full_name="The Dummy", email="The Dummy@test.com", group_id=3)
    user2.set_password("The Dummy_password")

    session.add(user)
    session.add(user2)
    session.commit()

    test_user = session.query(User).filter_by(full_name="test_user").first()

    access_token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    # mock questionary
    with patch('questionary.confirm') as mock_confirm, \
            patch('questionary.print'):

        dummy = session.query(User).filter_by(full_name="The Dummy").first()

        # mock confirm
        mock_confirm.return_value.unsafe_ask.side_effect = [
            True
        ]

        assert dummy is not None, "\"The Dummy\" was not created in the DB"

        app.menu.user_controller.handle_delete_user(dummy, access_token)

        dummy = session.query(User).filter_by(full_name="The Dummy").first()

        assert dummy is None, "\"The Dummy\" still exist"

        assert mock_confirm.call_count == 1, f"""confirm called {
            mock_confirm.call_count}/1"""
