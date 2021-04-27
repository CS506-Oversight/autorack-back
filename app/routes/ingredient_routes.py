"""Ingredient routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import IngredientResponse, UpsertIngredientItemResponse
from app.data import IngredientController

from .path import EP_INGREDIENT

__all__ = ("blueprint_ingredient",)

blueprint_ingredient: Blueprint = Blueprint("ingredient", __name__)


@blueprint_ingredient.route(EP_INGREDIENT, methods=["POST", "GET"])
def handle_menu_item():
    req_method = request.method
    user_id = request.args.get("user_id", type=str)

    if req_method == "POST":
        data = json.loads(request.data)

        return handle_upsert_ingredient(
            user_id=user_id,
            payload=data["payload"],
            operation=POST_OPERATION + "/updated"
        )

    return handle_get_ingredients(user_id=user_id, operation=GET_OPERATION)


def handle_get_ingredients(user_id: str, operation: str):
    ingredients = IngredientController.get_ingredients(user_id=user_id)

    return IngredientResponse(ingredients=ingredients, user_id=user_id, operation=operation)


def handle_upsert_ingredient(payload: list, user_id: str, operation: str):
    IngredientController.upsert_ingredients(
        user_id=user_id,
        payload=payload,
    )

    return UpsertIngredientItemResponse(user_id=user_id, num_items=len(payload), operation=operation)
