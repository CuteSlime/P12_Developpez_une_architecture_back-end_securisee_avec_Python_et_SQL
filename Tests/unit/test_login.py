from unittest.mock import patch
from Models import User


def test_user_login(app, session):
    """Create an user and use it to try the login"""

    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    with patch('questionary.text') as mock_text, \
            patch('questionary.print'), \
            patch('questionary.password') as mock_password, \
            patch.object(app.menu, 'main_menu') as mock_main_menu:

        mock_text.return_value.unsafe_ask.return_value = "test_user"
        mock_password.return_value.unsafe_ask.return_value = "test_password"

        app.menu.login()

        test_user = session.query(User).filter_by(
            full_name="test_user").first()

        assert test_user is not None, "test_user was not created in the DB"

        assert test_user.check_password(
            "test_password"), "encrypted password didn't match"

        assert mock_text.call_count == 1, "Questionary input was not called"
        assert mock_password.call_count == 1, "Questionary password input was not called"

        assert mock_main_menu.called, "Login didn't call the main menu"
