import json

from app.routes.path import EP_MENU_ITEM
from app.routes.operations import *


def test_menu_add_item(client):
    user_id = "kjhgvjklerlsjoife"
    payload = {
        "payload": [
            {
                "name": "new item name",
                "description": "new item desc",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            }
        ]
    }

    response = client.post(EP_MENU_ITEM + f'?user_id={user_id}', data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {POST_OPERATION+'/updated'} {len(payload['payload'])} menu items. (User: {user_id})"


def test_menu_add_two_items(client):
    user_id = "kjhgvjklerlsjoife"
    payload = {
        "payload": [
            {
                "name": "new item name 1",
                "description": "new_item",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            },
            {
                "name": "new item name 2",
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

    response = client.post(EP_MENU_ITEM + f'?user_id={user_id}', data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == \
           f"User {POST_OPERATION + '/updated'} {len(payload['payload'])} menu items. (User: {user_id})"


def test_menu_get_menu_multiple_items(client):
    user_id = "jkdsnkfkwdfhkjoc"
    post_payload = {
        "payload": [
            {
                "name": "new name",
                "description": "new_item1",
                "ingredients": [
                    {
                        "ingredient_id": "i_jkkkkjkkjkjkljlkjl",
                        "some_stuff": "nnnnnnnnnnnnn"
                    }
                ]
            },
            {
                "name": "new name",
                "description": "new_item_2",
                "ingredients": [
                    {
                        "ingredient_id": "i_pppp",
                        "some_stuff": "zzz"
                    }
                ]
            },
            {
                "name": "new name",
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

    client.post(EP_MENU_ITEM + f'?user_id={user_id}', data=json.dumps(post_payload))

    get_response = client.get(EP_MENU_ITEM + f'?user_id={user_id}')

    assert get_response.json["ok"]
    assert get_response.status_code == 200
    assert get_response.json["message"] == f"Menu {GET_OPERATION}. (User: {user_id})"
    assert len(get_response.json["data"]) == 3


def test_menu_get_empty_menu(client):
    user_id = "jkdsnkfkwdfhkjoc"

    response = client.get(EP_MENU_ITEM + f'?user_id={user_id}')

    assert response.json["ok"]
    assert response.status_code == 200
    # Checks if data is empty which it should be
    assert not response.json["data"]


def test_menu_update_menu_item(client):
    user_id = "kjhgvjklerlsjoife"
    post_payload = {
        "payload": [
            {
                "name": "item name",
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

    client.post(EP_MENU_ITEM + f'?user_id={user_id}', data=json.dumps(post_payload))

    get_response = client.get(EP_MENU_ITEM + f'?user_id={user_id}')

    menu_item_id = get_response.json["data"][0]["id"]

    update_payload = {
        "payload": [
            {
                "id": menu_item_id,
                "name": "UPDATED NAME",
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

    client.post(EP_MENU_ITEM + f'?user_id={user_id}', data=json.dumps(update_payload))
    update_response = client.get(EP_MENU_ITEM + f'?user_id={user_id}')

    assert update_response.json["ok"]
    assert update_response.status_code == 200
    assert update_response.json["message"] == f"Menu {GET_OPERATION}. (User: {user_id})"
    assert (get_response.json["data"][0]["description"] == "NEW ITEM") \
           and (update_response.json["data"][0]["description"] == "UPDATED ITEM")
    assert get_response.json["data"][0]["ingredients"] == update_response.json["data"][0]["ingredients"]
