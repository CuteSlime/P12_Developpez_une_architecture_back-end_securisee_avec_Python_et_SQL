from unittest.mock import patch
from Models import User


def test_token_check_expired_token(app):
    """Test token check when the token is expired."""

    access_token = "expired_token"

    # Mock the decode_access_token to return "expired", mock questionary and the login function
    with patch.object(User, 'decode_access_token', return_value="expired"), \
            patch('questionary.print'), \
            patch.object(app.menu, 'login', return_value=None) as mock_login:

        result = app.menu.token_check(access_token)

        assert mock_login.call_count == 1, "login was not called"
        assert result is None, "Token check should trigger login and return None for expired token"


def test_token_check_invalid_token(app):
    """Test token check when the token is invalid."""

    access_token = "invalid_token"

    # Mock the decode_access_token to return "expired", mock questionary and the login function
    with patch.object(User, 'decode_access_token', return_value=None), \
            patch('questionary.print'), \
            patch.object(app.menu, 'login', return_value=None) as mock_login:

        result = app.menu.token_check(access_token)

        assert mock_login.call_count == 1, "login was not called"
        assert result is None, "Token check should trigger login and return None for invalid token"


def test_token_check_valid_token(app):
    """Test token check when the token is valid."""

    access_token = "valid_token"
    decoded_token = {"role": "Management"}

    # Mock the decode_access_token to return {"role": "Management"} and the login function
    with patch.object(User, 'decode_access_token', return_value=decoded_token), \
            patch.object(app.menu, 'login') as mock_login:

        result = app.menu.token_check(access_token)

        assert mock_login.call_count == 0, "login was called (should not)"
        assert result == decoded_token["role"], "Token check should return the role for a valid token"
