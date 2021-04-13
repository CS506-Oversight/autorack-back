"""Menu routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import MenuItemResponse, MenuResponse, MenuControlFailedResponse, AddMenuItemResponse
from app.data import MenuController

from .path import EP_MENU, EP_MENU_ITEM

__all__ = ("blueprint_menu",)

blueprint_menu: Blueprint = Blueprint("menu", __name__)


@blueprint_menu.route(EP_MENU_ITEM, methods=["GET", "POST", "DELETE", "PATCH"])
def handle_menu_item():
    data = json.loads(request.data)
    req_method = request.method

    if req_method == "POST":
        return handle_add_menu_item(
            user_id=data["user_id"],
            payload=data["payload"],
            operation=POST_OPERATION
        )
    elif req_method == "DELETE":
        return handle_delete_menu_item(
            user_id=data["user_id"],
            menu_item_id=data["menu_item_id"],
            operation=DELETE_OPERATION
        )
    elif req_method == "PATCH":
        return handle_update_menu_item(
            user_id=data["user_id"],
            menu_item_id=data["menu_item_id"],
            operation=GET_OPERATION
        )
    else:
        return handle_get_menu_item(
            user_id=data["user_id"],
            menu_item_id=data["menu_item_id"],
            operation=GET_OPERATION
        )


@blueprint_menu.route(EP_MENU, methods=["GET"])
def handle_menu():
    data = json.loads(request.data)
    user_id = data["user_id"]

    return handle_get_menu(user_id=user_id, operation=GET_OPERATION)


def handle_get_menu_item(user_id: str, menu_item_id: str, operation: str):
    menu_item = MenuController.get_menu_item(user_id=user_id, menu_item_id=menu_item_id)

    if not menu_item:
        return MenuControlFailedResponse(message=f"Failed to get menu item {menu_item_id} for user {user_id}")

    return MenuItemResponse(menu_item=menu_item, operation=operation)


def handle_get_menu(user_id: str, operation: str):
    menu = MenuController.get_menu(user_id=user_id)

    if not menu:
        return MenuControlFailedResponse(message=f"Failed to get menu for user with user_id: {user_id}")

    return MenuResponse(menu=menu, user_id=user_id, operation=operation)


def handle_add_menu_item(payload: list, user_id: str, operation: str):
    new_menu_item = MenuController.add_menu_items(
        user_id=user_id,
        payload=payload,
    )

    if not new_menu_item:
        return MenuControlFailedResponse(message=f"Failed to add menu item(s) for user with user_id: {user_id}")

    return AddMenuItemResponse(user_id=user_id, num_items=len(payload), operation=operation)


def handle_delete_menu_item(user_id: str, menu_item_id: str, operation: str):
    # TODO: IMPLEMENT DELETE ROUTE FOR MENU ITEMS
    pass


def handle_update_menu_item(user_id: str, menu_item_id: str, operation: str):
    # TODO: IMPLEMENT UPDATE ROUTE FOR MENU ITEMS
    pass
