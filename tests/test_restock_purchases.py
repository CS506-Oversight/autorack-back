import json

from app.routes.path import EP_RESTOCK
from app.routes.operations import *
from app.data import RestockPurchaseController, RestockPurchaseModel


def test_restock_get_empty_restock_purchases(client):
    payload = {
        "user_id": "kjhgvjklerlsjoife"
    }

    response = client.get(EP_RESTOCK, data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {GET_OPERATION} 0 restock purchases. (User: {payload['user_id']})"


def test_restock_add_three_restock_purchases():
    user_id = "kjhgvjklerlsjoife"
    purchases = [
        {
            "status": "completed",
            "total_price": 1290.69,
            "purchase_date": "2017-11-01 00:00:00",
            "purchase_type": "Manual",
            "items_purchased": [
                {
                    "description": "Cheese Curds",
                    "unitPrice": 5.25,
                    "quantity": 50
                },
                {
                    "description": "Steak",
                    "unitPrice": 20.0,
                    "quantity": 35
                },
                {
                    "description": "Aquafina Water",
                    "unitPrice": 9.75,
                    "quantity": 25
                }
            ]
        },
        {
            "status": "completed",
            "total_price": 1290.69,
            "purchase_date": "2017-11-01 00:00:00",
            "purchase_type": "Auto",
            "items_purchased": [
                {
                    "description": "Cheese Curds",
                    "unitPrice": 5.25,
                    "quantity": 50
                },
                {
                    "description": "Steak",
                    "unitPrice": 20.0,
                    "quantity": 35
                },
                {
                    "description": "Aquafina Water",
                    "unitPrice": 9.75,
                    "quantity": 25
                }
            ]
        },
        {
            "status": "completed",
            "total_price": 1290.69,
            "purchase_date": "2017-11-01 00:00:00",
            "purchase_type": "Manual",
            "items_purchased": [
                {
                    "description": "Cheese Curds",
                    "unitPrice": 5.25,
                    "quantity": 50
                },
                {
                    "description": "Steak",
                    "unitPrice": 20.0,
                    "quantity": 35
                },
                {
                    "description": "Aquafina Water",
                    "unitPrice": 9.75,
                    "quantity": 25
                }
            ]
        },
    ]

    for purchase in purchases:
        assert RestockPurchaseController.add_restock_purchase(
            status=purchase["status"], total_price=purchase["total_price"], purchase_date=purchase["purchase_date"],
            purchase_type=["purchase_type"], items_purchased=purchase["items_purchased"], user_id=user_id
        )


def test_restock_add_one_check_price(client):
    user_id = "kjhgvjklerlsjoife"
    purchase = {
        "status": "completed",
        "total_price": 12.11,
        "purchase_date": "2017-11-01 00:00:00",
        "purchase_type": "Manual",
        "items_purchased": [
            {
                "description": "Cheese Curds",
                "unitPrice": 5.25,
                "quantity": 50
            },
            {
                "description": "Steak",
                "unitPrice": 20.0,
                "quantity": 35
            },
            {
                "description": "Aquafina Water",
                "unitPrice": 9.75,
                "quantity": 25
            }
        ]
    }

    assert RestockPurchaseController.add_restock_purchase(
        status=purchase["status"], total_price=purchase["total_price"], purchase_date=purchase["purchase_date"],
        purchase_type=["purchase_type"], items_purchased=purchase["items_purchased"], user_id=user_id
    )

    query_data = RestockPurchaseController.get_query().filter_by(user_id=user_id).all()

    assert len(query_data) == 1

    total_price = query_data[0].total_price
    assert total_price == (purchase["total_price"] * 100) == 1211

    response = client.get(EP_RESTOCK, data=json.dumps({"user_id": user_id}))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {GET_OPERATION} 1 restock purchases. (User: {user_id})"
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["total_price"] == purchase["total_price"] == (total_price / 100)


def test_restock_add_two_check_items_purchased(client):
    user_id = "kjhgvjklerlsjoife"
    purchases = [
        {
            "status": "completed",
            "total_price": 12.11,
            "purchase_date": "2017-11-01 00:00:00",
            "purchase_type": "Manual",
            "items_purchased": [
                {
                    "description": "Cheese Curds",
                    "unitPrice": 5.25,
                    "quantity": 50
                },
                {
                    "description": "Steak",
                    "unitPrice": 20.0,
                    "quantity": 35
                },
                {
                    "description": "Aquafina Water",
                    "unitPrice": 9.75,
                    "quantity": 25
                }
            ]
        },
        {
            "status": "completed",
            "total_price": 5.11,
            "purchase_date": "2017-11-01 00:00:00",
            "purchase_type": "Manual",
            "items_purchased": [
                {
                    "description": "Cheese Curds",
                    "unitPrice": 5.25,
                    "quantity": 50
                },
                {
                    "description": "Steak",
                    "unitPrice": 20.0,
                    "quantity": 35
                },
                {
                    "description": "Aquafina Water",
                    "unitPrice": 9.75,
                    "quantity": 25
                },
                {
                    "description": "Cheese Curds",
                    "unitPrice": 5.25,
                    "quantity": 50
                },
                {
                    "description": "Steak",
                    "unitPrice": 20.0,
                    "quantity": 35
                },
                {
                    "description": "Aquafina Water",
                    "unitPrice": 9.75,
                    "quantity": 25
                }
            ]
        }
    ]

    for purchase in purchases:
        assert RestockPurchaseController.add_restock_purchase(
            status=purchase["status"], total_price=purchase["total_price"], purchase_date=purchase["purchase_date"],
            purchase_type=["purchase_type"], items_purchased=purchase["items_purchased"], user_id=user_id
        )

    response = client.get(EP_RESTOCK, data=json.dumps({"user_id": user_id}))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {GET_OPERATION} 2 restock purchases. (User: {user_id})"
    assert len(response.json["data"]) == 2
    assert len(response.json["data"][0]["items_purchased"]) == 3
    assert len(response.json["data"][1]["items_purchased"]) == 6
