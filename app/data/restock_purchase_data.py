"""Data model and controller for restock purchases."""
import datetime
import json

from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base import Controller
from .config import db
from app.utils import generate_rand_id

__all__ = ("RestockPurchaseModel", "RestockPurchaseController")


class RestockPurchaseModel(db.Model):
    """Data model for restock purchases."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "restock_purchase"

    purchase_id = db.Column(db.String(), primary_key=True)
    status = db.Column(db.String(), nullable=False)
    # Should be stored in pennies for precision
    total_price = db.Column(db.Integer(), nullable=False)
    purchase_date = db.Column(db.DateTime(), nullable=False)
    purchase_type = db.Column(db.String(), nullable=False)
    # Should be saved as a serialized JSON object
    items_purchased = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.String(), nullable=False)

    def __init__(self, purchase_id: str, status: str, total_price: int, purchase_date: datetime, purchase_type: str,
                 items_purchased: str, user_id: str):
        self.purchase_id = purchase_id
        self.status = status
        self.total_price = total_price
        self.purchase_date = purchase_date
        self.purchase_type = purchase_type
        self.items_purchased = items_purchased
        self.user_id = user_id

    def __repr__(self):
        return f"<Purchase {self.purchase_id}>"

    def to_dict(self):
        items_purchased_deserialized = json.loads(self.items_purchased)
        serialized_date = str(self.purchase_date)

        return {
                "purchase_id": self.purchase_id,
                "status": self.status,
                "total_price": self.total_price / 100,
                "purchase_date": serialized_date,
                "purchase_type": self.purchase_type,
                "items_purchased": items_purchased_deserialized,
        }


class RestockPurchaseController(Controller):
    """Controller for restock purchases."""

    model = RestockPurchaseModel

    @classmethod
    def add_restock_purchase(cls, status: str, total_price: int, purchase_date: datetime,
                             purchase_type: str, items_purchased: list, user_id: str) -> bool:
        """
        Add a restock purchase and return when the purchase is added.
        """
        session: Session = cls.get_session()

        items_purchased_serialized = json.dumps(items_purchased)

        # Generate random purchase_id for new restock purchase
        random_purchase_id = generate_rand_id("p_")
        while cls.__item_exists(user_id=user_id, purchase_id=random_purchase_id):
            random_purchase_id = generate_rand_id("p_")

        purchase = RestockPurchaseModel(
            purchase_id=random_purchase_id,
            status=status,
            total_price=total_price * 100,
            purchase_date=purchase_date,
            purchase_type=purchase_type,
            items_purchased=items_purchased_serialized,
            user_id=user_id
        )

        session.add(purchase)
        session.commit()

        return True

    @classmethod
    def get_restock_purchases(cls, user_id: str) -> list:
        """Gets the restock purchases for user with ``user_id``."""
        query_data = cls.get_query().filter_by(user_id=user_id).all()

        restock_purchases = [data.to_dict() for data in query_data]

        return restock_purchases

    @classmethod
    def __item_exists(cls, user_id: str, purchase_id: str) -> bool:
        """
        Private function that checks if a menu item exists. Returns true
        if the item exists, else false if the item exists.
        """
        return cls.get_query().filter(
            and_(
                RestockPurchaseModel.purchase_id == purchase_id,
                RestockPurchaseModel.user_id == user_id
            )
        ).first() is not None
