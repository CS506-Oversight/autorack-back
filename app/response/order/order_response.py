"""Response classes for the main routes."""
from dataclasses import dataclass
from typing import Any


from app.response.keys import KEY_DATA
from app.response.mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = ("OrderResponse", "UpsertOrderResponse")


@dataclass
class UpsertOrderResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for orders."""

    user_id: str
    num_items: int
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"User {self.operation} {self.num_items} orders. (User: {self.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

@dataclass
class OrderResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for orders."""

    order: list
    operation: str
    user_id: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `menu_item` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"Order {self.operation}. (User: {self.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_DATA: self.order
        }