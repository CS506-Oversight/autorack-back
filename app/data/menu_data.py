"""Data model and controller for menu."""
import json
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.utils import generate_rand_id
from .base import Controller
from .config import db

__all__ = ("MenuModel", "MenuController")


class MenuModel(db.Model):
    """Data model for menu."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "menu"

    menu_item_id = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.String(), nullable=False)
    # Should be a serialized JSON object
    ingredients = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=True)

    def __init__(self, menu_item_id: str, description: str, ingredients: str, user_id: str, name: str):
        self.menu_item_id = menu_item_id
        self.description = description
        self.ingredients = ingredients
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"<Menu_Item {self.menu_item_id}>"

    def to_dict(self):
        ingredients = json.loads(self.ingredients)

        return {
            "id": self.menu_item_id,
            "description": self.description,
            "ingredients": ingredients,
            "name": self.name
        }


class MenuController(Controller):
    """Controller for menu."""

    model = MenuModel

    @classmethod
    def upsert_menu_items(cls, user_id: str, payload: list) -> bool:
        """
        Add/update a menu item and return true or false when the item is added.
        """
        session: Session = cls.get_session()

        for item in payload:
            ingredients_to_str = json.dumps(item["ingredients"])

            # If menu_item_id is in payload, this is an update, else a new addition
            if "id" in item:
                cls.__update(
                    menu_item_id=item["id"],
                    user_id=user_id,
                    new_description=item["description"],
                    new_ingredients=ingredients_to_str,
                    new_name=item["name"],
                    session=session
                )

                continue

            # Generate random menu_item_id for new menu_item
            random_menu_id = generate_rand_id("m_")
            while cls.__item_exists(user_id=user_id, menu_item_id=random_menu_id):
                random_menu_id = generate_rand_id("m_")

            menu_item = MenuModel(
                menu_item_id=random_menu_id,
                description=item["description"],
                ingredients=ingredients_to_str,
                user_id=user_id,
                name=item["name"]
            )

            session.add(menu_item)

        session.commit()

        return True

    @classmethod
    def get_menu(cls, user_id: str) -> list:
        """Gets the entire menu for user with ``user_id``."""
        query_data = cls.get_query().filter_by(user_id=user_id).all()

        menu = [data.to_dict() for data in query_data]

        return menu

    @classmethod
    def __item_exists(cls, user_id: str, menu_item_id: str) -> bool:
        """
        Private function that checks if a menu item exists. Returns true
        if the item exists, else false if the item exists.
        """
        return cls.get_query().filter(
            and_(
                MenuModel.menu_item_id == menu_item_id,
                MenuModel.user_id == user_id
            )
        ).first() is not None

    @classmethod
    def __update(cls, menu_item_id: str, user_id: str, new_description: str, new_ingredients: str,
                 new_name: str, session: Session) -> None:
        """
        Private function that updates the details of a menu item. Users are only able to
        Update the description and ingredients of a menu item
        """
        session.query(MenuModel).filter(
            and_(
                MenuModel.user_id == user_id,
                MenuModel.menu_item_id == menu_item_id
            )
        ).update(
            {
                "description": new_description,
                "ingredients": new_ingredients,
                "name": new_name
            }
        )

        session.commit()
