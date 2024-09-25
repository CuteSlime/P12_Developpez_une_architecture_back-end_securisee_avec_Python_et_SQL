from datetime import timedelta

from Models import User


def test_token_creation(session):
    """Test token creation"""
    user = User(full_name="test_user", email="test@test.com", group_id=1)
    user.set_password("test_password")

    session.add(user)
    session.commit()

    test_user = session.query(User).filter_by(
        full_name="test_user").first()

    token = User.create_access_token(
        data={"username": test_user.full_name, "role": test_user.role.group_name})

    token_with_timer = User.create_access_token(
        data={"username": test_user.full_name,
              "role": test_user.role.group_name},
        expires_delta=(timedelta(minutes=10))
    )
    token_expired = User.create_access_token(
        data={"username": test_user.full_name,
              "role": test_user.role.group_name},
        expires_delta=(timedelta(minutes=-10))
    )
    decoded_token = User.decode_access_token(token)
    decoded_token_with_timer = User.decode_access_token(token_with_timer)
    bad_token = User.decode_access_token("bad")
    bad_token_timer = User.decode_access_token(token_expired)

    assert decoded_token["role"] == "Management"
    assert decoded_token["username"] == "test_user"
    assert decoded_token_with_timer["role"] == "Management"
    assert decoded_token_with_timer["username"] == "test_user"
    assert bad_token_timer == "expired"
    assert bad_token is None
