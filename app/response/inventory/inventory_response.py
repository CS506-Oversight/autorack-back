"""Response classes for inventory routes."""
from dataclasses import dataclass
from typing import Any

from app.response.keys import KEY_DATA
from app.response.mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = "InventoryResponse"


@dataclass
class InventoryResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for retrieving inventory."""

    inventory: list
    user_id: str
    operation: str

    @property
    def response_message(self) -> str:
        return f"Inventory {self.operation}. (User: {self.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_DATA: self.inventory
        }
