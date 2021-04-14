"""Ingredient routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import IngredientResponse, IngredientControlFailedResponse, UpsertIngredientItemResponse
from app.data import IngredientController

from .path import EP_INGREDIENT

__all__ = ("blueprint_ingredient",)

blueprint_ingredient: Blueprint = Blueprint("ingredient", __name__)


@blueprint_ingredient.route(EP_INGREDIENT, methods=["POST", "DELETE", "GET"])
def handle_menu_item():
    data = json.loads(request.data)
    req_method = request.method
    user_id = data["user_id"]

    if req_method == "POST":
        return handle_upsert_ingredient(
            user_id=user_id,
            payload=data["payload"],
            operation=POST_OPERATION
        )
    elif req_method == "DELETE":
        return handle_delete_menu_item(
            user_id=user_id,
            ingredient_id=data["ingredient_id"],
            operation=DELETE_OPERATION
        )
    else:
        return handle_get_ingredients(user_id=user_id, operation=GET_OPERATION)


def handle_get_ingredients(user_id: str, operation: str):
    ingredients = IngredientController.get_ingredients(user_id=user_id)

    return IngredientResponse(ingredients=ingredients, user_id=user_id, operation=operation)


def handle_upsert_ingredient(payload: list, user_id: str, operation: str):
    new_ingredient = IngredientController.upsert_ingredients(
        user_id=user_id,
        payload=payload,
    )

    # if not new_menu_item:
    #     return IngredientControlFailedResponse(message=f"Failed to add/update menu item(s) for user: {user_id}")

    return UpsertIngredientItemResponse(user_id=user_id, num_items=len(payload), operation=operation+'/updated')


def handle_delete_menu_item(user_id: str, ingredient_id: str, operation: str):
    # TODO: IMPLEMENT DELETE ROUTE FOR INGREDIENT
    pass
