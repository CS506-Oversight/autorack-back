"""Response classes for the main routes."""
from dataclasses import dataclass
from typing import Any

from app.data import MealModel

from .keys import KEY_RESULT
from .mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = ("RootResponse", "SimpleAddResponse", "MealAddedResponse")


@dataclass
class RootResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for the root endpoint."""

    message: str
    ok: bool

    @property
    def response_message(self) -> str:
        return self.message

    @property
    def response_ok(self) -> bool:
        return self.ok


@dataclass
class SimpleAddResponse(StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for the simple addition endpoint."""

    result: int

    @property
    def response_ok(self) -> bool:
        return True  # Always True

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_RESULT: self.result
        }


@dataclass
class MealAddedResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class of successfully adding a meal."""

    meal: MealModel

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `meal` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"Meal added. (Name: {self.meal.name})"

    @property
    def response_ok(self) -> bool:
        return True
