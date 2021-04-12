"""Response classes for the main routes."""
from dataclasses import dataclass
from typing import Any

from .keys import KEY_RESULT
from .mixin import MessagedResponseMixin, StatusedResponseMixin, HttpOkResponseMixin

__all__ = "RootResponse"


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
