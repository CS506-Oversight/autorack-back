"""Response classes for the main routes."""
import json
from dataclasses import dataclass
from typing import Any

from app.data import MenuModel

from app.response.keys import KEY_DATA
from app.response.mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = ("MenuItemResponse", "MenuResponse")

# TODO: ADDED RESPONSE CLASSES TO HANDLE CHANGES IN ROUTES


@dataclass
class MenuItemResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for menu items."""

    menu_item: MenuModel
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"Menu item {self.operation}. (Menu item: {self.menu_item.menu_item_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        # TODO: FIND CORRECT WAY TO SEND THIS DATA BACK
        data = json.dumps({
                'menu_item_id': self.menu_item.menu_item_id,
                'ingredients': self.menu_item.ingredients,
                'description': self.menu_item.description,
        })

        return super().to_json() | {
            KEY_DATA: data
        }


@dataclass
class MenuResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for menu."""

    menu: MenuModel
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"Menu {self.operation}. (User: {self.menu.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        # TODO: FIND CORRECT WAY TO SEND THIS DATA BACK
        data = 'MENU DATA'

        return super().to_json() | {
            KEY_DATA: data
        }
