import json
from datetime import datetime

from app.routes.path import EP_USER
from app.routes.operations import *

now = datetime.now()
timestamp = int(datetime.timestamp(now))


def test_user_add_user(client):

    user_id = "ckjdscoie8uf9vodlkj"

    payload = {
        "id": user_id,
        "firstName": "TEST_FIRST_NAME",
        "lastName": "TEST_LAST_NAME",
        "createdAt": timestamp,
        "email": "test_user@gmail.com",
    }

    response = client.post(EP_USER, data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"User {POST_OPERATION}. (User: {user_id})"
    assert response.json["data"] == {
        "id": user_id,
        "email": payload["email"],
        "firstName": payload["firstName"],
        "lastName": payload["lastName"]
    }


def test_user_add_two_users(client):
    payload = [
        {
            "id": "jhbfjdknvoflkjdsllk",
            "firstName": "USER_1",
            "lastName": "USER_1_LAST",
            "createdAt": timestamp,
            "email": "user1@gmail.com",
        },
        {
            "id": "bckjdsbnovidajhbcjk",
            "firstName": "USER_2",
            "lastName": "USER_2_LAST",
            "createdAt": timestamp,
            "email": "user2@gmail.com",
        }
    ]

    for user in payload:
        response = client.post(EP_USER, data=json.dumps(user))

        assert response.json["ok"]
        assert response.status_code == 200
        assert response.json["message"] == f"User {POST_OPERATION}. (User: {user['id']})"
        assert response.json["data"] == {
            "id": user["id"],
            "email": user["email"],
            "firstName": user["firstName"],
            "lastName": user["lastName"]
        }


def test_user_add_two_get_two(client):
    payload = [
        {
            "id": "jhbfjdknvoflkjdsllk",
            "firstName": "USER_1",
            "lastName": "USER_1_LAST",
            "createdAt": timestamp,
            "email": "user1@gmail.com",
        },
        {
            "id": "bckjdsbnovidajhbcjk",
            "firstName": "USER_2",
            "lastName": "USER_2_LAST",
            "createdAt": timestamp,
            "email": "user2@gmail.com",
        }
    ]

    for user in payload:
        client.post(EP_USER, data=json.dumps(user))
        response = client.get(EP_USER + f"?user_id={user['id']}")

        assert response.json["ok"]
        assert response.status_code == 200
        assert response.json["message"] == f"User {GET_OPERATION}. (User: {user['id']})"
        assert response.json["data"] == {
            "id": user["id"],
            "email": user["email"],
            "firstName": user["firstName"],
            "lastName": user["lastName"]
        }


def test_user_get_user(client):
    user_id = "ckjdscoie8uf9vodlkj"

    post_payload = {
        "id": user_id,
        "firstName": "TEST_FIRST_NAME",
        "lastName": "TEST_LAST_NAME",
        "createdAt": timestamp,
        "email": "test_user@gmail.com",
    }

    client.post(EP_USER, data=json.dumps(post_payload))
    response = client.get(EP_USER + f"?user_id={user_id}")

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"User {GET_OPERATION}. (User: {user_id})"
    assert response.json["data"] == {
        "id": user_id,
        "email": post_payload["email"],
        "firstName": post_payload["firstName"],
        "lastName": post_payload["lastName"]
    }


def test_user_get_unexisting_user(client):
    user_id = "nhkhfkjklsjfpwofp"

    response = client.get(EP_USER + f"?user_id={user_id}")

    assert not response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"Failed to get user with user_id: {user_id}. User may not exist."
