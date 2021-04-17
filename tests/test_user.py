import json

from app.routes.path import EP_USER
from app.routes.operations import *


def test_user_add_user(client):
    payload = {
        "user_id": "ckjdscoie8uf9vodlkj",
        "first_name": "TEST_FIRST_NAME",
        "last_name": "TEST_LAST_NAME",
        "created_at": "2021-04-11 12:37:53.052393",
        "email": "test_user@gmail.com",
    }

    response = client.post(EP_USER, data=json.dumps(payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"User {POST_OPERATION}. (User: {payload['user_id']})"
    assert response.json["data"] == {
        "user_id": payload["user_id"],
        "email": payload["email"],
        "first_name": payload["first_name"],
    }


def test_user_add_two_users(client):
    payload = [
        {
            "user_id": "jhbfjdknvoflkjdsllk",
            "first_name": "USER_1",
            "last_name": "USER_1_LAST",
            "created_at": "2021-04-11 12:37:53.052393",
            "email": "user1@gmail.com",
        },
        {
            "user_id": "bckjdsbnovidajhbcjk",
            "first_name": "USER_2",
            "last_name": "USER_2_LAST",
            "created_at": "2021-04-11 12:37:53.052393",
            "email": "user2@gmail.com",
        }
    ]

    for user in payload:
        response = client.post(EP_USER, data=json.dumps(user))

        assert response.json["ok"]
        assert response.status_code == 200
        assert response.json["message"] == f"User {POST_OPERATION}. (User: {user['user_id']})"
        assert response.json["data"] == {
            "user_id": user["user_id"],
            "email": user["email"],
            "first_name": user["first_name"],
        }


def test_user_add_two_get_two(client):
    payload = [
        {
            "user_id": "jhbfjdknvoflkjdsllk",
            "first_name": "USER_1",
            "last_name": "USER_1_LAST",
            "created_at": "2021-04-11 12:37:53.052393",
            "email": "user1@gmail.com",
        },
        {
            "user_id": "bckjdsbnovidajhbcjk",
            "first_name": "USER_2",
            "last_name": "USER_2_LAST",
            "created_at": "2021-04-11 12:37:53.052393",
            "email": "user2@gmail.com",
        }
    ]

    for user in payload:
        client.post(EP_USER, data=json.dumps(user))
        response = client.get(EP_USER, data=json.dumps({"user_id": user["user_id"]}))

        assert response.json["ok"]
        assert response.status_code == 200
        assert response.json["message"] == f"User {GET_OPERATION}. (User: {user['user_id']})"
        assert response.json["data"] == {
            "user_id": user["user_id"],
            "email": user["email"],
            "first_name": user["first_name"],
        }


def test_user_get_user(client):
    post_payload = {
        "user_id": "ckjdscoie8uf9vodlkj",
        "first_name": "TEST_FIRST_NAME",
        "last_name": "TEST_LAST_NAME",
        "created_at": "2021-04-11 12:37:53.052393",
        "email": "test_user@gmail.com",
    }

    get_payload = {
        "user_id": post_payload["user_id"]
    }

    client.post(EP_USER, data=json.dumps(post_payload))
    response = client.get(EP_USER, data=json.dumps(get_payload))

    assert response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"User {GET_OPERATION}. (User: {post_payload['user_id']})"
    assert response.json["data"] == {
        "user_id": post_payload["user_id"],
        "email": post_payload["email"],
        "first_name": post_payload["first_name"],
    }


def test_user_get_unexisting_user(client):
    payload = {
        "user_id": "nhkhfkjklsjfpwofp"
    }

    response = client.get(EP_USER, data=json.dumps(payload))

    assert not response.json["ok"]
    assert response.status_code == 200
    assert response.json["message"] == f"Failed to get user with user_id: {payload['user_id']}. User may not exist."
