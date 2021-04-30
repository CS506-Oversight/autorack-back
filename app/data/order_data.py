"""Data model and controller for orders."""
import json
import datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.utils import generate_rand_id
from .base import Controller
from .config import db

__all__ = ("OrderModel", "OrderController")


class OrderModel(db.Model):
    """Data model for order."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "order"

    order_id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), nullable=False)
    # Should be a serialized JSON object
    order = db.Column(db.String(), nullable=True)
    date = db.Column(db.String(), nullable=False)

    def __init__(self, order_id: str, order: str, user_id: str):
        self.order_id = order_id
        self.order = order
        self.user_id = user_id
        self.date = datetime.datetime.now()

    def __repr__(self):
        return f"<Order {self.order_id}>"

    def to_dict(self):
        order = json.loads(self.order)

        return {
            "order_id": self.order_id,
            "order": order,
        }


class OrderController(Controller):
    """Controller for orders."""

    model = OrderModel

    @classmethod
    def upsert_order(cls, user_id: str, payload: list) -> bool:
        """
        Add/update an order and return true or false when the order is added.
        """
        session: Session = cls.get_session()
        ordered_items_to_str = ''
        for item in payload:
            ordered_items_to_str += json.dumps(item)
        random_order_id = generate_rand_id("o_")
        while cls.__order_exists(user_id=user_id, order_id=random_order_id):
            random_order_id = generate_rand_id("o_")

        final_order = OrderModel(
            order_id=random_order_id,
            order=ordered_items_to_str,
            user_id=user_id,
        )
        session.add(final_order)
        session.commit()

    @classmethod
    def get_orders(cls, user_id: str) -> list:
        """Gets all orders for user with ``user_id``."""
        query_data = cls.get_query().filter_by(user_id=user_id).all()

        orders = [data.to_dict() for data in query_data]

        return orders

    @classmethod
    def __order_exists(cls, user_id: str, order_id: str) -> bool:
        """
        Private function that checks if an order exists. Returns true
        if the order exists, else false if the order exists.
        """
        return cls.get_query().filter(
            and_(
                OrderModel.order_id == order_id,
                OrderModel.user_id == user_id
            )
        ).first() is not None
