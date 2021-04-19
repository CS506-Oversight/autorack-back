"""User routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import UserResponse, UserControlFailedResponse
from app.data import UserController

from .path import EP_USER

__all__ = ("blueprint_user",)

blueprint_user: Blueprint = Blueprint("user", __name__)


@blueprint_user.route(EP_USER, methods=["GET", "POST"])
def handle_user():
    req_method = request.method

    if req_method == "POST":
        data = json.loads(request.data)

        return handle_add(
            user_id=data["id"],
            first_name=data["firstName"],
            last_name=data["lastName"],
            created_at=data['createdAt'],
            email=data['email'],
            operation=POST_OPERATION
        )

    user_id = request.args.get("user_id", type=str)

    return handle_get(user_id=user_id, operation=GET_OPERATION)


def handle_get(user_id: str, operation: str):
    """ Handles get requests for users. """
    user = UserController.get_user(user_id=user_id)

    if not user:
        return UserControlFailedResponse(message=f"Failed to get user with user_id: {user_id}. User may not exist.")

    return UserResponse(user=user, operation=operation)


def handle_add(user_id: str, first_name: str, last_name: str, created_at: int, email: str, operation: str):
    """ Handles post requests for users. """
    new_user = UserController.add_user(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        created_at=created_at,
        email=email
    )

    user = UserController.get_user(user_id)

    if not user:
        return UserControlFailedResponse(message=f"Failed to retrieve user with user_id: {user_id}")

    return UserResponse(user=user, operation=operation)
