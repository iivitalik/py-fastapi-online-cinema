import pytest


@pytest.mark.anyio
async def test_access_protected_route_without_token(client):
    response = await client.get("/movies/")
    assert response.status_code == 401