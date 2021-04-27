"""Response classes for the main routes."""
import json
from dataclasses import dataclass
from typing import Any

from app.data import UserModel

from app.response.keys import KEY_DATA
from app.response.mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = "UserResponse"


@dataclass
class UserResponse(MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin):
    """Response class for user."""

    user: UserModel
    operation: str

    @property
    def response_message(self) -> str:
        # [!] Does not handle the case where `meal` is `None`
        # because our type-hinting indicates that there *must* be a model for `meal`
        return f"User {self.operation}. (User: {self.user.user_id})"

    @property
    def response_ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_DATA: self.user.to_dict()
        }
