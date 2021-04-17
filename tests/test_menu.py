import json

from app.routes.path import EP_MENU_ITEM
from app.routes.operations import *


def test_menu_add_item(client):
    payload = {
        "user_id": "kjhgvjklerlsjoife",
        "payload": [
            {
                "description": "new_item",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            }
        ]
    }

    response = client.post(EP_MENU_ITEM, data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {POST_OPERATION+'/updated'} {len(payload['payload'])} menu items. (User: {payload['user_id']})"


def test_menu_add_two_items(client):
    payload = {
        "user_id": "kjhgvjklerlsjoife",
        "payload": [
            {
                "description": "new_item",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            },
            {
                "description": "new_item_2",
                "ingredients": [
                    {
                        "ingredient_id": "i_pppp",
                        "some_stuff": "zzz"
                    }
                ]
            }
        ]
    }

    response = client.post(EP_MENU_ITEM, data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {POST_OPERATION + '/updated'} {len(payload['payload'])} menu items. (User: {payload['user_id']})"


def test_menu_get_menu_multiple_items(client):
    post_payload = {
        "user_id": "jkdsnkfkwdfhkjoc",
        "payload": [
            {
                "description": "new_item1",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            },
            {
                "description": "new_item_2",
                "ingredients": [
                    {
                        "ingredient_id": "i_pppp",
                        "some_stuff": "zzz"
                    }
                ]
            },
            {
                "description": "new_item_3",
                "ingredients": [
                    {
                        "ingredient_id": "i_fksljfsl",
                        "some_stuff": "mmmmmmm"
                    }
                ]
            },
        ]
    }

    client.post(EP_MENU_ITEM, data=json.dumps(post_payload))

    get_payload = {
        "user_id": "jkdsnkfkwdfhkjoc"
    }

    get_response = client.get(EP_MENU_ITEM, data=json.dumps(get_payload))

    assert get_response.json["ok"]
    assert get_response.status_code == 200
    assert get_response.json["message"] == f"Menu {GET_OPERATION}. (User: {get_payload['user_id']})"
    assert len(get_response.json["data"]) == 3


def test_menu_get_empty_menu(client):
    payload = {
        "user_id": "jkdsnkfkwdfhkjoc"
    }

    response = client.get(EP_MENU_ITEM, data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    # Checks if data is empty which it should be
    assert not response.json["data"]


def test_menu_update_menu_item(client):
    post_payload = {
        "user_id": "kjhgvjklerlsjoife",
        "payload": [
            {
                "description": "NEW ITEM",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            }
        ]
    }

    client.post(EP_MENU_ITEM, data=json.dumps(post_payload))

    get_payload = {
        "user_id": "kjhgvjklerlsjoife",
    }

    get_response = client.get(EP_MENU_ITEM, data=json.dumps(get_payload))

    menu_item_id = get_response.json["data"][0]["menu_item_id"]

    update_payload = {
        "user_id": "kjhgvjklerlsjoife",
        "payload": [
            {
                "menu_item_id": menu_item_id,
                "description": "UPDATED ITEM",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            }
        ]
    }

    client.post(EP_MENU_ITEM, data=json.dumps(update_payload))
    update_response = client.get(EP_MENU_ITEM, data=json.dumps({"user_id": "kjhgvjklerlsjoife"}))

    assert update_response.json["ok"]
    assert update_response.status_code == 200
    assert update_response.json["message"] == f"Menu {GET_OPERATION}. (User: {update_payload['user_id']})"
    assert (get_response.json["data"][0]["description"] == "NEW ITEM") \
           and (update_response.json["data"][0]["description"] == "UPDATED ITEM")
    assert get_response.json["data"][0]["ingredients"] == update_response.json["data"][0]["ingredients"]
