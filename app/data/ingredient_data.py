"""Data model and controller for ingredients."""
import json

from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.utils import generate_rand_id
from .base import Controller
from .supplier_data import SupplierController
from .config import db

__all__ = ("IngredientModel", "IngredientController")


class IngredientModel(db.Model):
    """Data model for ingredients."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.String(), primary_key=True)
    measurement = db.Column(db.String(), nullable=False)
    current_stock = db.Column(db.Numeric(10, 2), nullable=False)
    current_stock_equivalent = db.Column(db.Numeric(10, 2), nullable=False)
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.String(), nullable=False)
    capacity = db.Column(db.Numeric(10, 2), nullable=False)
    capacity_equivalent = db.Column(db.Numeric(10, 2), nullable=False)
    capacity_measure = db.Column(db.String(), nullable=False)

    def __init__(self, ingredient_id: str, measurement: str, current_stock: float, user_id: str, name: str,
                 capacity: float, capacity_equivalent: float, capacity_measure: str, current_stock_equivalent: float):
        self.ingredient_id = ingredient_id
        self.measurement = measurement
        self.capacity = capacity
        self.user_id = user_id
        self.name = name
        self.capacity_equivalent = capacity_equivalent
        self.capacity_measure = capacity_measure
        self.current_stock_equivalent = current_stock_equivalent
        self.current_stock = current_stock

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id}>"

    def to_dict(self):
        measure_deserialized = json.loads(self.measurement)
        capacity_measure_deserialized = json.loads(self.capacity_measure)

        return {
            "name": self.name,
            "id": self.ingredient_id,
            "measure": measure_deserialized,
            "currentStock": float(self.current_stock),
            "capacity": float(self.capacity),
            "capacityEquivalent": float(self.capacity_equivalent),
            "capacityMeasure": capacity_measure_deserialized,
            "currentStockEquivalent": float(self.current_stock_equivalent),
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
            capacity_measure_serialized = json.dumps(item["capacityMeasure"])
            # If ingredient_id already exists, then this is an update
            if "id" in item:
                ingredient_id = item["id"]

                # Update the ingredient
                cls.__update(
                    ingredient_id=ingredient_id,
                    user_id=user_id,
                    new_current_stock=item["currentStock"],
                    new_measurement=measure_serialized,
                    new_name=item["name"],
                    new_capacity=item["capacity"],
                    new_capacity_equivalent=item["capacityEquivalent"],
                    new_capacity_measure=capacity_measure_serialized,
                    new_current_stock_equivalent=item["currentStockEquivalent"],
                    session=session
                )

                continue

            # Get random id for ingredient
            rand_ingredient_id = generate_rand_id("i_")
            while cls.__item_exists(user_id=user_id, ingredient_id=rand_ingredient_id):
                rand_ingredient_id = generate_rand_id("i_")

            SupplierController.add_ingredient(ingredient_id=rand_ingredient_id, measure=item["measure"])

            ingredient = IngredientModel(
                ingredient_id=rand_ingredient_id,
                measurement=measure_serialized,
                current_stock=item["currentStock"],
                user_id=user_id,
                name=item["name"],
                capacity=item["capacity"],
                capacity_equivalent=item["capacityEquivalent"],
                capacity_measure=capacity_measure_serialized,
                current_stock_equivalent=item["currentStockEquivalent"],
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
    def __update(cls, ingredient_id: str, user_id: str, new_current_stock: int, new_measurement: str,
                 new_name: str, new_capacity: int, new_capacity_equivalent: float, new_capacity_measure: str,
                 new_current_stock_equivalent: float, session: Session) -> None:
        session.query(IngredientModel).filter(
            and_(
                IngredientModel.user_id == user_id,
                IngredientModel.ingredient_id == ingredient_id
            )
        ).update(
            {
                "current_stock": new_current_stock,
                "measurement": new_measurement,
                "name": new_name,
                "capacity": new_capacity,
                "capacity_equivalent": new_capacity_equivalent,
                "capacity_measure": new_capacity_measure,
                "current_stock_equivalent": new_current_stock_equivalent,
            }
        )

        session.commit()
