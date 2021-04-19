"""Restock purchases routes."""
import json
from flask import Blueprint, request

from .operations import *
from app.response import RestockPurchaseResponse
from app.data import RestockPurchaseController

from .path import EP_RESTOCK

__all__ = ("blueprint_restock_purchase",)

blueprint_restock_purchase: Blueprint = Blueprint("restock_purchase", __name__)


@blueprint_restock_purchase.route(EP_RESTOCK, methods=["GET"])
def get_restock_purchases():
    user_id = request.args.get("user_id", type=str)

    restock_purchases = RestockPurchaseController.get_restock_purchases(user_id=user_id)

    return RestockPurchaseResponse(restock_purchases=restock_purchases, user_id=user_id, operation=GET_OPERATION)
