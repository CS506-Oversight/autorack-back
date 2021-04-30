"""Order routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import OrderResponse, UpsertOrderResponse
from app.data import OrderController
from app.inventory import InventoryController

from .path import EP_ORDER

__all__ = ("blueprint_order",)

blueprint_order: Blueprint = Blueprint("order", __name__)


@blueprint_order.route(EP_ORDER, methods=["GET", "POST"])
def handle_order():
    user_id = request.args.get("user_id", type=str)
    data = json.loads(request.data)
    InventoryController.update_inventory(data["payload"], user_id)
    req_method = request.method

    if req_method == "POST":
        return handle_upsert_order(
            user_id=user_id,
            payload=data["payload"],
            operation=POST_OPERATION + "/updated"
        )
    return handle_get_orders(user_id=user_id, operation=GET_OPERATION)


def handle_get_orders(user_id: str, operation: str):
    order = OrderController.get_orders(user_id=user_id)

    return OrderResponse(order=order, user_id=user_id, operation=operation)


def handle_upsert_order(payload: list, user_id: str, operation: str):
    new_order = OrderController.upsert_order(
        user_id=user_id,
        payload=payload,
    )

    return UpsertOrderResponse(user_id=user_id, num_items=len(payload), operation=operation)