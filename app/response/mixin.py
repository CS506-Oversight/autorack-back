"""Mixins for the response classes."""
from abc import ABC
from dataclasses import dataclass
from typing import Any

from .base import ResponseBase
from .keys import KEY_MESSAGE, KEY_OK

__all__ = ("MessagedResponseMixin", "StatusedResponseMixin", "HttpOkResponseMixin")


@dataclass
class HttpOkResponseMixin(ResponseBase, ABC):
    """Mixin for the response that returns HTTP status code 200."""

    @property
    def http_status(self) -> int:
        return 200


@dataclass
class MessagedResponseMixin(ResponseBase, ABC):
    """Mixin for the response class that has a message."""

    @property
    def response_message(self) -> str:
        """Message of the response."""
        raise NotImplementedError()

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_MESSAGE: self.response_message
        }


@dataclass
class StatusedResponseMixin(ResponseBase, ABC):
    """Mixin for the response class that has a status."""

    @property
    def response_ok(self) -> bool:
        """If the response is "OK"."""
        raise NotImplementedError()

    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {
            KEY_OK: self.response_ok
        }


@dataclass
class FailedResponse(MessagedResponseMixin, StatusedResponseMixin, ABC):
    """Response class for a failing response."""

    error_message: str

    @property
    def response_message(self) -> str:
        return self.error_message

    @property
    def response_ok(self) -> bool:
        return False
