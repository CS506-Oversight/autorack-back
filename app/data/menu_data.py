"""Data model and controller for menu."""
import json
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

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

    def __init__(self, menu_item_id: str, description: str, ingredients: str, user_id: str):
        self.menu_item_id = menu_item_id
        self.description = description
        self.ingredients = ingredients
        self.user_id = user_id

    def __repr__(self):
        return f"<Menu_Item {self.menu_item_id}>"

    def to_dict(self):
        ingredients = json.loads(self.ingredients)

        return {
            "menu_item_id": self.menu_item_id,
            "description": self.description,
            "ingredients": ingredients,
        }


class MenuController(Controller):
    """Controller for menu."""

    model = MenuModel

    @classmethod
    def upsert_menu_items(cls, user_id: str, payload: list) -> bool:
        """
        Add/update a menu item and return true or false when the item is added.
        """
        # TODO: MAY NEED TO ADD ROLLBACKS HERE JUST IN CASE

        session: Session = cls.get_session()

        for item in payload:
            ingredients_to_str = json.dumps(item["ingredients"])
            menu_item_id = item["menu_item_id"]

            menu_item = cls.__item_exists(user_id=user_id, menu_item_id=menu_item_id)

            if menu_item:
                cls.__update(
                    menu_item_id=menu_item.menu_item_id,
                    user_id=menu_item.user_id,
                    new_description=item["description"],
                    new_ingredients=ingredients_to_str,
                    session=session
                )
            else:
                menu_item = MenuModel(
                    menu_item_id=menu_item_id,
                    description=item["description"],
                    ingredients=ingredients_to_str,
                    user_id=user_id,
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

    # @classmethod
    # def delete_menu_item(cls, menu_item_id: str, user_id: str) -> MenuModel:
    #     """TODO: Delete the menu item with ``menu_item_id`` for user with ``user_id``.."""
    #     pass

    @classmethod
    def __item_exists(cls, user_id: str, menu_item_id: str) -> Optional[MenuModel]:
        return cls.get_query().filter(
            and_(
                MenuModel.menu_item_id == menu_item_id,
                MenuModel.user_id == user_id
            )
        ).first()

    @classmethod
    def __update(cls, menu_item_id: str, user_id: str, new_description: str, new_ingredients: str,
                 session: Session) -> None:
        session.query(MenuModel).filter(
            and_(
                MenuModel.user_id == user_id,
                MenuModel.menu_item_id == menu_item_id
            )
        ).update(
            {
                "description": new_description,
                "ingredients": new_ingredients
            }
        )

        session.commit()
