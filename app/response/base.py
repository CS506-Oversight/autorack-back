"""Base response class."""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, final

from flask import Response

from app.base import JsonSerializable

__all__ = ("ResponseBase",)


@dataclass
class ResponseBase(JsonSerializable, ABC):
    """
    Base response class.

    This is **not** a Flask response. To get the Flask response from this class,
    call ``to_flask_response()``.

    This should not be directly used.
    Instead, create a class inherited from this class and instantiate that class instead.
    """

    @abstractmethod
    def to_json(self) -> dict[str, Any]:
        """
        Convert this class to a json object.

        The return of this will be used as the response content when converting to a Flask response.
        """
        return {}

    @property
    @abstractmethod
    def http_status(self) -> int:
        """HTTP status code of this response."""
        raise NotImplementedError()

    @final
    def to_flask_response(self) -> Response:
        """Convert this response object to Flask response object."""
        return Response(json.dumps(self.to_json()), mimetype="application/json", status=self.http_status)
