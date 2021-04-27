from app.routes.path import EP_ROOT


def test_root(client):
    """Ping the root endpoint."""
    response = client.get(EP_ROOT)

    assert response.status_code == 200
    assert response.json["ok"]
