"""Data model and controller for ingredients."""
import json

from sqlalchemy.orm import Session
from sqlalchemy import and_

from .ingredient_data import IngredientModel, IngredientController
from .base import Controller
from .config import db

__all__ = ("IngredientsInProgressModel", "IngredientInProgressController")


class IngredientsInProgressModel(db.Model):
    """Data model for ingredients in progress."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "ingredients_in_progress"

    ingredient_id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    amount_in_progress = db.Column(db.Numeric(10, 2), nullable=False)
    amount_in_progress_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    user_id = db.Column(db.String(), nullable=False)

    def __init__(self, ingredient_id: str, name: str, amount_in_progress: float, amount_in_progress_percentage: float,
                 user_id: str):
        self.ingredient_id = ingredient_id
        self.name = name
        self.amount_in_progress = amount_in_progress
        self.user_id = user_id
        self.amount_in_progress_percentage = amount_in_progress_percentage

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id}>"


class IngredientInProgressController(Controller):
    """Controller for ingredients in progress."""

    model = IngredientsInProgressModel

    @classmethod
    def add_ingredients_in_progress(cls, user_id: str, name: str, ingredient_id: str, amount_in_progress: float,
                                    amount_in_progress_percentage: float) -> bool:
        session: Session = cls.get_session()

        ingredient_in_progress = IngredientsInProgressModel(
            ingredient_id=ingredient_id,
            name=name,
            amount_in_progress=amount_in_progress,
            amount_in_progress_percentage=amount_in_progress_percentage,
            user_id=user_id
        )

        session.add(ingredient_in_progress)

        session.commit()

        return True

    @classmethod
    def get_ingredients_in_progress(cls, user_id: str) -> list:
        """Gets inventory for user with ``user_id``."""
        ingredients = IngredientController.get_ingredients(user_id=user_id)
        data = []

        for ingredient in ingredients:
            curr_stock_data = cls.get_in_stock_data(ingredient=ingredient)
            in_progress_data = cls.get_query().filter(
                and_(
                    IngredientsInProgressModel.ingredient_id == ingredient["id"],
                    IngredientsInProgressModel.user_id == user_id
                )
            ).first()

            in_progress = 0.0 if not in_progress_data else in_progress_data.amount_in_progress
            in_progress_percentage = 0.0 if not in_progress_data else in_progress_data.amount_in_progress_percentage

            data.append({
                "name": ingredient["name"],
                "id": ingredient["id"],
                "amountInProgress": float(in_progress),
                "amountInProgressPercentage": float(in_progress_percentage),
                "amountInStock": curr_stock_data[0],
                "amountInStockPercentage": curr_stock_data[1]
            })

        return data

    @classmethod
    def get_in_stock_data(cls, ingredient: dict) -> tuple:
        """Gets all ingredients in progress for user with ``user_id``."""
        curr_stock = float(ingredient["currentStock"])
        curr_stock_decimal = float(ingredient["currentStockEquivalent"]) / float(ingredient["capacityEquivalent"])
        curr_stock_percentage = float(100) * curr_stock_decimal

        return curr_stock, curr_stock_percentage

    @classmethod
    def delete_ingredients_in_progress(cls, user_id: str, ingredient_id: str):
        """Deletes ingredient in progress for user with ``user_id``."""
        session: Session = cls.get_session()

        ingredient_in_progress = cls.get_query().filter(
            and_(
                IngredientsInProgressModel.ingredient_id == ingredient_id,
                IngredientsInProgressModel.user_id == user_id
            )).first()

        session.delete(ingredient_in_progress)
        session.commit()
