"""Interface for a json serializable object."""
from abc import ABC, abstractmethod
from typing import Any

__all__ = ("JsonSerializable",)


class JsonSerializable(ABC):
    """Interface for a json serializable object."""

    # Just an interface
    # pylint: disable=too-few-public-methods

    @abstractmethod
    def to_json(self) -> dict[str, Any]:
        """Convert this object to json object."""
        raise NotImplementedError()
