"""Data model and controller for ingredients."""
from sqlalchemy.orm import Session

from .base import Controller
from .config import db

__all__ = ("IngredientModel", "IngredientController")


class IngredientModel(db.Model):
    """Data model for ingredients."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.String(), primary_key=True)
    measurement = db.Column(db.String(), nullable=False)
    unit = db.Column(db.Integer(), nullable=False)
    unit_price = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.String(), nullable=False)

    def __init__(self, ingredient_id: str, measurement: str, unit: int, unit_price: int, user_id: str):
        self.ingredient_id = ingredient_id
        self.measurement = measurement
        self.unit = unit
        self.unit_price = unit_price
        self.user_id = user_id

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id}>"


class IngredientController(Controller):
    """Controller for ingredients."""

    model = IngredientModel

    @classmethod
    def add_ingredient(cls, measurement: str, unit: int, unit_price: int, user_id: str) -> bool:
        """
        Add an ingredient and return true or false when the ingredient is added.
        """
        session: Session = cls.get_session()

        ingredient_id = ''  # TODO: SHOULD BE GENERATED RANDOMLY

        ingredient = IngredientModel(
            ingredient_id=ingredient_id,
            measurement=measurement,
            unit=unit,
            unit_price=unit_price,
            user_id=user_id,
        )

        session.add(ingredient)
        session.commit()

        return True

    @classmethod
    def get_ingredient(cls, ingredient_id: str, user_id: str) -> IngredientModel:
        """Gets the ingredient with ``ingredient_id`` for user with ``user_id``."""
        pass

    @classmethod
    def get_ingredients(cls, user_id: str) -> IngredientModel:
        """Gets all the ingredients for user with ``user_id``."""
        pass

    @classmethod
    def update_ingredient(cls, ingredient_id: str, user_id: str) -> IngredientModel:
        """Updates the ingredient with ``ingredient_id`` for user with ``user_id``."""
        pass

    @classmethod
    def delete_ingredient(cls, ingredient_id: str, user_id: str) -> IngredientModel:
        """Deletes the ingredient with ``ingredient_id`` for user with ``user_id``."""
        pass
