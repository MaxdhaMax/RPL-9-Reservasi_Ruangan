from WebApp import bcrypt


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    assert new_user.email == "locationtest@locat.com"
    assert new_user.username == "locationtest"
    assert bcrypt.check_password_hash(
        new_user.password, "locationtest123") == True
