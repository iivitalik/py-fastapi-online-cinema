from app import utils

def test_password_hashing():
    password = "secret_password"
    hashed = utils.hash_password(password)
    assert hashed != password
    assert utils.verify_password(password, hashed) is True

def test_invalid_password_verification():
    hashed = utils.hash_password("correct_pass")
    assert utils.verify_password("wrong_pass", hashed) is False