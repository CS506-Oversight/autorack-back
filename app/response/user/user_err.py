"""Erroneous response classes."""
from dataclasses import dataclass

from ..mixin import MessagedResponseMixin, StatusedResponseMixin

__all__ = ("UserControlFailedResponse",)


@dataclass
class UserControlFailedResponse(MessagedResponseMixin, StatusedResponseMixin):
    """Response class for the failing response of user control."""

    message: str

    @property
    def http_status(self) -> int:
        return 200

    @property
    def response_ok(self) -> bool:
        return False

    @property
    def response_message(self) -> str:
        return self.message
