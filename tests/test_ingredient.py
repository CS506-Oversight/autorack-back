import json

from app.routes.path import EP_INGREDIENT
from app.routes.operations import *


def test_ingredient_add_item(client):
    user_id = "jRD9JUG1fzMP3FoMopfIivfgBh42"
    payload = {
        "payload": [
            {
                "name": "Chicken",
                "measure": {
                    "name": "lb",
                    "equivalentMetric": 453.592,
                    "type": 1
                },
                "currentStock": 50.00,
                "currentStockEquivalent": 22679.60,
                "capacity": 50.00,
                "capacityEquivalent": 22679.60,
                "capacityMeasure":
                    {
                        "name": "lb",
                        "equivalentMetric": 453.592,
                        "type": 1
                    }
            }
        ]
    }

    response = client.post(EP_INGREDIENT + f'?user_id={user_id}', data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {POST_OPERATION + '/updated'} {len(payload['payload'])} ingredients. (User: {user_id})"


def test_ingredient_add_two_items(client):
    user_id = "jRD9JUG1fzMP3FoMopfIivfgBh42"
    payload = {
        "payload": [
            {
                "name": "Chicken",
                "measure": {
                    "name": "lb",
                    "equivalentMetric": 453.592,
                    "type": 1
                },
                "currentStock": 50.00,
                "currentStockEquivalent": 22679.60,
                "capacity": 50.00,
                "capacityEquivalent": 22679.60,
                "capacityMeasure":
                    {
                        "name": "lb",
                        "equivalentMetric": 453.592,
                        "type": 1
                    }
            },
            {
                "name": "Tree Bark",
                "measure": {
                    "name": "lb",
                    "equivalentMetric": 453.592,
                    "type": 1
                },
                "currentStock": 1000.00,
                "currentStockEquivalent": 453592,
                "capacity": 1000.00,
                "capacityEquivalent": 453592,
                "capacityMeasure":
                    {
                        "name": "lb",
                        "equivalentMetric": 453.592,
                        "type": 1
                    }
            },
        ]
    }

    response = client.post(EP_INGREDIENT + f'?user_id={user_id}', data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {POST_OPERATION + '/updated'} {len(payload['payload'])} ingredients. (User: {user_id})"


def test_ingredient_get_multiple_ingredients(client):
    user_id = "jRD9JUG1fzMP3FoMopfIivfgBh42"
    payload = {
        "payload": [
            {
                "name": "Chicken",
                "measure": {
                    "name": "lb",
                    "equivalentMetric": 453.592,
                    "type": 1
                },
                "currentStock": 50.00,
                "currentStockEquivalent": 22679.60,
                "capacity": 50.00,
                "capacityEquivalent": 22679.60,
                "capacityMeasure":
                    {
                        "name": "lb",
                        "equivalentMetric": 453.592,
                        "type": 1
                    }
            },
            {
                "name": "Tree Bark",
                "measure": {
                    "name": "lb",
                    "equivalentMetric": 453.592,
                    "type": 1
                },
                "currentStock": 1000.00,
                "currentStockEquivalent": 453592,
                "capacity": 1000.00,
                "capacityEquivalent": 453592,
                "capacityMeasure":
                    {
                        "name": "lb",
                        "equivalentMetric": 453.592,
                        "type": 1
                    }
            },
        ]
    }

    client.post(EP_INGREDIENT + f'?user_id={user_id}', data=json.dumps(payload))

    response = client.get(EP_INGREDIENT + f'?user_id={user_id}')

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"Ingredients {GET_OPERATION}. (User: {user_id})"
    assert len(response.json["data"]) == 2


def test_ingredients_get_empty_ingredients(client):
    user_id = "jRD9JUG1fzMP3FoMopfIivfgBh42"

    response = client.get(EP_INGREDIENT + f'?user_id={user_id}')

    assert response.json["ok"]
    assert response.status_code == 200
    # Checks if data is empty which it should be
    assert not response.json["data"]
#
#
# def test_ingredient_update_ingredient(client):
#     pass
