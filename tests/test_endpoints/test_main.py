from app.routes.path import EP_ROOT, EP_ADD, EP_DATA


def test_root(client):
    """Ping the root endpoint."""
    response = client.get(EP_ROOT)

    assert response.status_code == 200
    assert response.json["ok"]


def test_add(client):
    """Test the simple addition calculation endpoint."""
    payload = {
        "arg1": 1,
        "arg2": 5
    }

    response = client.get(EP_ADD, query_string=payload)

    assert response.status_code == 200
    assert response.json["result"] == 6


def test_data_add_meal(client):
    """Test the dummy data endpoint."""
    meal_name = "Meal"

    payload = {
        "mealName": meal_name,
    }

    response = client.get(EP_DATA, query_string=payload)

    assert response.status_code == 200
    assert response.json["ok"]
    assert response.json["message"] == f"Meal added. (Name: {meal_name})"


def test_data_add_meal_empty_name(client):
    """Test the dummy data endpoint, but does not provide a meal name."""
    meal_name = ""

    payload = {
        "mealName": meal_name,
    }

    response = client.get(EP_DATA, query_string=payload)

    assert response.status_code == 200
    assert not response.json["ok"]
    assert response.json["message"] == f"Failed to add a meal with name: "
