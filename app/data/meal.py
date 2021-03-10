"""Data model and controller for meals."""
from sqlalchemy.orm import Session

from .base import Controller
from .config import db

__all__ = ("MealModel", "MealController")


class MealModel(db.Model):
    """Data model for meals."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "meal"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Meal {self.name}>"


class MealController(Controller):
    """Controller for meals."""

    model = MealModel

    @classmethod
    def add_meal(cls, name: str) -> bool:
        """
        Add a meal named as ``name`` and return if the meal is added or not.

        If ``name`` is falsy (empty string or ``None``),
        this directly returns ``False`` without performing any additional actions.
        """
        if not name:
            return False  # Empty name, do not add the meal

        session: Session = cls.get_session()

        model = MealModel(name=name)

        _: list[bool] = []

        session.add(model)
        session.commit()

        return True

    @classmethod
    def get_meal(cls, name: str) -> MealModel:
        """Get the meal with ``name``."""
        # [!] model member `query` is generated automatically, therefore auto-complete is unavailable.
        # - Reference: https://stackoverflow.com/a/39103583/11571888
        return cls.get_query().filter_by(name=name).first()
