"""Data model and controller for supplier."""
import random as rand

from sqlalchemy.orm import Session

from .base import Controller
from .config import db

__all__ = ("SupplierModel", "SupplierController")


class SupplierModel(db.Model):
    """Data model for supplier."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "supplier"

    ingredient_id = db.Column(db.String(), primary_key=True)
    ingredient_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, ingredient_id: str, ingredient_price: float):
        self.ingredient_id = ingredient_id
        self.ingredient_price = ingredient_price

    def __repr__(self):
        return f"<Ingredient (Supplier) {self.ingredient_id}>"


class SupplierController(Controller):
    """Controller for supplier."""

    model = SupplierModel

    @classmethod
    def add_ingredient(cls, ingredient_id: str, measure: str) -> bool:
        session: Session = cls.get_session()

        random_price = 0.0
        measure_name = measure["name"]
        measure_type = measure["type"]

        if measure_type == 1:
            if measure_name == "lb":
                random_price = round(rand.uniform(0.60, 5.75), 2)
            elif measure_name == "oz" or measure_name == "g":
                random_price = round(rand.uniform(0.05, 0.75), 2)
        else:
            random_price = round(rand.uniform(0.05, 0.25), 2)

        new_ingredient = SupplierModel(ingredient_id=ingredient_id, ingredient_price=random_price)

        session.add(new_ingredient)
        session.commit()

        return True

    @classmethod
    def get_ingredient_price(cls, ingredient_id: str) -> float:
        ingredient = cls.get_query().filter_by(ingredient_id=ingredient_id).first()
        return float(ingredient.ingredient_price)
