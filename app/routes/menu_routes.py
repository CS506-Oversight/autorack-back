"""Menu routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import MenuItemResponse, MenuResponse, MenuControlFailedResponse, UpsertMenuItemResponse
from app.data import MenuController

from .path import EP_MENU, EP_MENU_ITEM

__all__ = ("blueprint_menu",)

blueprint_menu: Blueprint = Blueprint("menu", __name__)


@blueprint_menu.route(EP_MENU_ITEM, methods=["POST", "DELETE", "PATCH"])
def handle_menu_item():
    data = json.loads(request.data)
    req_method = request.method

    if req_method == "POST" or req_method == "PATCH":
        operation = POST_OPERATION if req_method == "POST" else PATCH_OPERATION

        return handle_upsert_menu_item(
            user_id=data["user_id"],
            payload=data["payload"],
            operation=operation
        )
    elif req_method == "DELETE":
        return handle_delete_menu_item(
            user_id=data["user_id"],
            menu_item_id=data["menu_item_id"],
            operation=DELETE_OPERATION
        )


@blueprint_menu.route(EP_MENU, methods=["GET"])
def handle_menu():
    data = json.loads(request.data)
    user_id = data["user_id"]

    return handle_get_menu(user_id=user_id, operation=GET_OPERATION)


def handle_get_menu(user_id: str, operation: str):
    menu = MenuController.get_menu(user_id=user_id)

    return MenuResponse(menu=menu, user_id=user_id, operation=operation)


def handle_upsert_menu_item(payload: list, user_id: str, operation: str):
    new_menu_item = MenuController.upsert_menu_items(
        user_id=user_id,
        payload=payload,
    )

    # if not new_menu_item:
    #     return MenuControlFailedResponse(message=f"Failed to add/update menu item(s) for user with user_id: {user_id}")

    return UpsertMenuItemResponse(user_id=user_id, num_items=len(payload), operation=operation+'/updated')


def handle_delete_menu_item(user_id: str, menu_item_id: str, operation: str):
    # TODO: IMPLEMENT DELETE ROUTE FOR MENU ITEMS
    pass
