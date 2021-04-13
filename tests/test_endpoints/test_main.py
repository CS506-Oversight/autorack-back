from app.routes.path import EP_ROOT


def test_root(client):
    """Ping the root endpoint."""
    response = client.get(EP_ROOT)

    assert response.status_code == 200
    assert response.json["ok"]


# def test_data_add_meal(client):
#     """Test the dummy data endpoint."""
#     meal_name = "Meal"
#
#     payload = {
#         "mealName": meal_name,
#     }
#
#     response = client.get(EP_DATA, query_string=payload)
#
#     assert response.status_code == 200
#     assert response.json["ok"]
#     assert response.json["message"] == f"Meal added. (Name: {meal_name})"


# def test_data_add_meal_empty_name(client):
#     """Test the dummy data endpoint, but does not provide a meal name."""
#     meal_name = ""
#
#     payload = {
#         "mealName": meal_name,
#     }
#
#     response = client.get(EP_DATA, query_string=payload)
#
#     assert response.status_code == 200
#     assert not response.json["ok"]
#     assert response.json["message"] == f"Failed to add a meal with name: "
