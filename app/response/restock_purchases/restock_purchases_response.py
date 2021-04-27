"""Response classes for the restock purchases routes."""
import json
from dataclasses import dataclass
from typing import Any

from app.response.keys import KEY_DATA
from app.response.mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = "RestockPurchaseResponse"


@dataclass
class RestockPurchaseResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for restock purchases."""

    restock_purchases: list
    user_id: str
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `menu_item`
        return f"User {self.operation} {len(self.restock_purchases)} restock purchases. (User: {self.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_DATA: self.restock_purchases
        }
