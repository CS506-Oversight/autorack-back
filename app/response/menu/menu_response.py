"""Response classes for the main routes."""
import json
from dataclasses import dataclass
from typing import Any

from app.data import MenuModel

from app.response.keys import KEY_DATA
from app.response.mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = ("MenuItemResponse", "MenuResponse", "AddMenuItemResponse")


@dataclass
class MenuItemResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for menu items."""

    menu_item: MenuModel
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `menu_item`
        return f"Menu item {self.operation}. (Menu item: {self.menu_item.menu_item_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        ingredients = json.loads(self.menu_item.ingredients)

        data = {
            "menu_item_id": self.menu_item.menu_item_id,
            "description": self.menu_item.description,
            "ingredients": ingredients,
        }

        return super().to_json() | {
            KEY_DATA: data
        }


@dataclass
class AddMenuItemResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for menu items."""

    user_id: str
    num_items: int
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"User {self.operation} {self.num_items} menu items. (User: {self.user_id})"

    @property
    def response_ok(self) -> bool:
        return True


@dataclass
class MenuResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for menu."""

    menu: list
    operation: str
    user_id: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"Menu {self.operation}. (User: {self.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_DATA: self.menu
        }
