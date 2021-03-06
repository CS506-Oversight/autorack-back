"""Inventory routes."""
from flask import Blueprint, request

from .operations import *
from app.response import InventoryResponse
from app.data import IngredientInProgressController
from app.inventory.update_inventory import InventoryController

from .path import EP_INVENTORY

__all__ = ("blueprint_inventory",)

blueprint_inventory: Blueprint = Blueprint("inventory", __name__)


@blueprint_inventory.route(EP_INVENTORY, methods=["GET", "POST"])
def handle_menu_item():
    user_id = request.args.get("user_id", type=str)

    if request.method == "POST":
        InventoryController.fulfill_inventory(user_id=user_id)
        return "Successful", 200

    return handle_get_ingredients(user_id=user_id, operation=GET_OPERATION)


def handle_get_ingredients(user_id: str, operation: str):
    inventory = IngredientInProgressController.get_ingredients_in_progress(user_id=user_id)
    return InventoryResponse(inventory=inventory, user_id=user_id, operation=operation)
