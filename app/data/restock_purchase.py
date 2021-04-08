"""Data model and controller for restock purchases."""
import datetime
from sqlalchemy.orm import Session

from .base import Controller
from .config import db

__all__ = ("RestockPurchaseModel", "RestockPurchaseController")


class RestockPurchaseModel(db.Model):
    """Data model for restock purchases."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "restock_purchase"

    purchase_id = db.Column(db.String(), primary_key=True)
    status = db.Column(db.String(), nullable=False)
    total_price = db.Column(db.Integer(), nullable=False)
    purchase_date = db.Column(db.DateTime(), nullable=False)
    purchase_type = db.Column(db.String(), nullable=False)
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


class RestockPurchaseController(Controller):
    """Controller for restock purchases."""

    model = RestockPurchaseModel

    @classmethod
    def add_restock_purchase(cls, purchase_id: str, status: str, total_price: int, purchase_date: datetime,
                             purchase_type: str, items_purchased: str, user_id: str) -> bool:
        """
        Add a restock purchase and return when the purchase is added.
        """
        session: Session = cls.get_session()

        model = RestockPurchaseModel(
            purchase_id=purchase_id,
            status=status,
            total_price=total_price,
            purchase_date=purchase_date,
            purchase_type=purchase_type,
            items_purchased=items_purchased,
            user_id=user_id
        )

        session.add(model)
        session.commit()

        return True

    @classmethod
    def get_restock_purchases(cls, user_id: str) -> RestockPurchaseModel:
        """Get the purchase with ``user_id``."""
        return cls.get_query().filter_by(user_id=user_id)
