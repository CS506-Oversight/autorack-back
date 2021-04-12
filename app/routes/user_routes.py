"""User routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import UserResponse, UserControlFailedResponse
from app.data import UserController

from .path import EP_USER

__all__ = ("blueprint_user",)

blueprint_user: Blueprint = Blueprint("user", __name__)


@blueprint_user.route(EP_USER, methods=["GET", "POST", "DELETE", "PATCH"])
def handle_user():
    data = json.loads(request.data)
    req_method = request.method

    if req_method == "POST":
        return handle_add(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            created_at=data['created_at'],
            email=data['email'],
            operation=POST_OPERATION
        )
    elif req_method == "DELETE":
        return handle_delete(user_id=data['user_id'], operation=DELETE_OPERATION)
    elif req_method == "PATCH":
        return handle_update(user_id=data['user_id'], operation=PATCH_OPERATION)
    else:
        return handle_get(user_id=data['user_id'], operation=GET_OPERATION)


def handle_get(user_id: str, operation: str):
    """ Handles get requests for users. """
    user = UserController.get_user(user_id=user_id)

    if not user:
        return UserControlFailedResponse(message=f"Failed to add user with email: {user_id}")

    return UserResponse(user=user, operation=operation)


def handle_add(user_id: str, first_name: str, last_name: str, created_at: str, email: str, operation: str):
    """ Handles post requests for users. """
    new_user = UserController.add_user(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        created_at=created_at,
        email=email
    )

    if not new_user:
        return UserControlFailedResponse(message=f"Failed to add user with email: {email}")

    user = UserController.get_user(user_id)

    if not user:
        return UserControlFailedResponse(message=f"User with user_id: {user_id}")

    return UserResponse(user=user, operation=operation)


def handle_update(user_id: str, operation: str):
    """ Handles patch requests for users. """
    pass


def handle_delete(user_id: str, operation: str):
    """ Handles delete requests for users. """
    user_deleted = UserController.delete_user(user_id=user_id)

    if not user_deleted:
        return UserControlFailedResponse(message=f"Failed to add user with email: {user_id}")

    return UserResponse(user=user_deleted, operation=operation)
