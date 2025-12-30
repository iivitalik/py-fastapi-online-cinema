import pytest


def test_password_hashing_logic():
    from app import utils
    password = "MySecurePassword123"
    hashed = utils.hash_password(password)
    assert hashed != password
    assert utils.verify_password(password, hashed) is True


@pytest.mark.anyio
async def test_registration_and_profile_creation(client):
    user_data = {
        "email": "test_user@example.com",
        "password": "Password123!"
    }

    response = await client.post("/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "User created" in data["message"]


@pytest.mark.anyio
async def test_login_fail_if_not_activated(client):
    user_data = {"email": "inactive@example.com", "password": "Password123!"}
    await client.post("/auth/register", json=user_data)

    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = await client.post("/auth/login", data=login_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Account not activated"