"""Data model and controller for menu."""
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


class MenuController(Controller):
    """Controller for menu."""

    model = MenuModel

    @classmethod
    def add_menu_items(cls, user_id: str, payload: list) -> bool:
        """
        Add a menu item and return true or false when the item is added.
        """
        # TODO: SEE IF THERE SHOULD BE SOME CHECK TO SEE HOW MANY WERE ADDED OUT OF ALL SENT
        session: Session = cls.get_session()

        for item in payload:
            menu_item = MenuModel(
                menu_item_id=item["menu_item_id"],
                description=item["description"],
                ingredients=item["ingredients"],
                user_id=user_id,
            )

            session.add(menu_item)

        session.commit()

        return True

    @classmethod
    def get_menu(cls, user_id: str) -> list:
        """Gets the entire menu for user with ``user_id``."""
        return cls.get_query().filter_by(user_id=user_id).all()

    @classmethod
    def get_menu_item(cls, menu_item_id: str, user_id: str) -> MenuModel:
        """Gets the menu item with ``menu_item_id`` for user with ``user_id``."""
        return cls.get_query().filter(
            and_(
                MenuModel.menu_item_id == menu_item_id,
                MenuModel.user_id == user_id
            )
        ).first()

    @classmethod
    def update_menu_item(cls, menu_item_id: str, user_id: str) -> MenuModel:
        """Updates the menu item with ``menu_item_id`` for user with ``user_id``."""
        pass

    @classmethod
    def delete_menu_item(cls, menu_item_id: str, user_id: str) -> MenuModel:
        """Deletes the menu item with ``menu_item_id`` for user with ``user_id``.."""
        pass
