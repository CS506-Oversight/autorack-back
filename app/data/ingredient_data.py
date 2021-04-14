"""Data model and controller for ingredients."""
import json
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

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
    name = db.Column(db.String(), nullable=False)
    unit_price = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.String(), nullable=False)

    def __init__(self, ingredient_id: str, measurement: str, unit: int, unit_price: int, user_id: str, name: str):
        self.ingredient_id = ingredient_id
        self.measurement = measurement
        self.unit = unit
        self.unit_price = unit_price
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id}>"

    def to_dict(self):
        return {
            "name": self.name,
            "ingredient_id": self.ingredient_id,
            "measurement": self.measurement,
            "unit": self.unit,
            "unit_price": self.unit_price / 100
        }


class IngredientController(Controller):
    """Controller for ingredients."""

    model = IngredientModel

    @classmethod
    def upsert_ingredients(cls, user_id: str, payload: list) -> bool:
        """
        Add/update an ingredient and return true or false when the ingredient is added.
        """
        session: Session = cls.get_session()

        for item in payload:
            ingredient_id = item["ingredient_id"]  # TODO: SHOULD BE GENERATED RANDOMLY

            ingredient = cls.__item_exists(user_id=user_id, ingredient_id=ingredient_id)

            if ingredient:
                cls.__update(
                    ingredient_id=ingredient.ingredient_id,
                    user_id=ingredient.user_id,
                    new_unit=item["unit"],
                    new_measurement=item["measurement"],
                    new_name=item["name"],
                    new_unit_price=item["unit_price"] * 100,
                    session=session
                )
            else:
                ingredient = IngredientModel(
                    ingredient_id=ingredient_id,
                    measurement=item["measurement"],
                    unit=item["unit"],
                    unit_price=item["unit_price"] * 100,
                    user_id=user_id,
                    name=item["name"]
                )

                session.add(ingredient)

        session.commit()

        return True

    @classmethod
    def get_ingredients(cls, user_id: str) -> list:
        """Gets all ingredients for user with ``user_id``."""
        query_data = cls.get_query().filter_by(user_id=user_id).all()

        ingredients = [data.to_dict() for data in query_data]

        return ingredients

    @classmethod
    def delete_ingredient(cls, ingredient_id: str, user_id: str) -> IngredientModel:
        """Deletes the ingredient with ``ingredient_id`` for user with ``user_id``."""
        pass

    @classmethod
    def __item_exists(cls, user_id: str, ingredient_id: str) -> Optional[IngredientModel]:
        return cls.get_query().filter(
            and_(
                IngredientModel.ingredient_id == ingredient_id,
                IngredientModel.user_id == user_id
            )
        ).first()

    @classmethod
    def __update(cls, ingredient_id: str, user_id: str, new_unit: int, new_measurement: str,
                 new_name: str, new_unit_price: int, session: Session) -> None:
        session.query(IngredientModel).filter(
            and_(
                IngredientModel.user_id == user_id,
                IngredientModel.ingredient_id == ingredient_id
            )
        ).update(
            {
                "unit": new_unit,
                "measurement": new_measurement,
                "unit_price": new_unit_price,
                "name": new_name
            }
        )

        session.commit()
