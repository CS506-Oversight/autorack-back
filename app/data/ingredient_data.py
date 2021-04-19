"""Data model and controller for ingredients."""
import json

from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.utils import generate_rand_id
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
    user_id = db.Column(db.String(), nullable=False)

    def __init__(self, ingredient_id: str, measurement: str, unit: int, user_id: str, name: str):
        self.ingredient_id = ingredient_id
        self.measurement = measurement
        self.unit = unit
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id}>"

    def to_dict(self):
        measure_deserialized = json.loads(self.measurement)

        return {
            "name": self.name,
            "id": self.ingredient_id,
            "measure": measure_deserialized,
            "unit": self.unit
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
            measure_serialized = json.dumps(item["measure"])
            # If ingredient_id already exists, then this is an update
            if "id" in item:
                ingredient_id = item["id"]

                # Update the ingredient
                cls.__update(
                    ingredient_id=ingredient_id,
                    user_id=user_id,
                    new_unit=item["unit"],
                    new_measurement=measure_serialized,
                    new_name=item["name"],
                    session=session
                )

                continue

            # Get random id for ingredient
            rand_ingredient_id = generate_rand_id("i_")
            while cls.__item_exists(user_id=user_id, ingredient_id=rand_ingredient_id):
                rand_ingredient_id = generate_rand_id("i_")

            ingredient = IngredientModel(
                ingredient_id=rand_ingredient_id,
                measurement=measure_serialized,
                unit=item["unit"],
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
    def __item_exists(cls, user_id: str, ingredient_id: str) -> bool:
        return cls.get_query().filter(
            and_(
                IngredientModel.ingredient_id == ingredient_id,
                IngredientModel.user_id == user_id
            )
        ).first() is not None

    @classmethod
    def __update(cls, ingredient_id: str, user_id: str, new_unit: int, new_measurement: str,
                 new_name: str, session: Session) -> None:
        session.query(IngredientModel).filter(
            and_(
                IngredientModel.user_id == user_id,
                IngredientModel.ingredient_id == ingredient_id
            )
        ).update(
            {
                "unit": new_unit,
                "measurement": new_measurement,
                "name": new_name
            }
        )

        session.commit()
