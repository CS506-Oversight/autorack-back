"""Menu routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import MenuResponse, UpsertMenuItemResponse
from app.data import MenuController

from .path import EP_MENU_ITEM

__all__ = ("blueprint_menu",)

blueprint_menu: Blueprint = Blueprint("menu", __name__)


@blueprint_menu.route(EP_MENU_ITEM, methods=["GET", "POST"])
def handle_menu_item():
    req_method = request.method

    if req_method == "POST":
        data = json.loads(request.data)
        user_id = data["id"]

        return handle_upsert_menu_item(
            user_id=user_id,
            payload=data["payload"],
            operation=POST_OPERATION + "/updated"
        )

    user_id = request.args.get("user_id", type=str)

    return handle_get_menu(user_id=user_id, operation=GET_OPERATION)


def handle_get_menu(user_id: str, operation: str):
    menu = MenuController.get_menu(user_id=user_id)

    return MenuResponse(menu=menu, user_id=user_id, operation=operation)


def handle_upsert_menu_item(payload: list, user_id: str, operation: str):
    new_menu_item = MenuController.upsert_menu_items(
        user_id=user_id,
        payload=payload,
    )

    return UpsertMenuItemResponse(user_id=user_id, num_items=len(payload), operation=operation)
