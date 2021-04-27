"""Main routes."""
from flask import Blueprint, request

from app.response import RootResponse

from .path import EP_ROOT

__all__ = ("blueprint_main",)

blueprint_main: Blueprint = Blueprint("main", __name__)


# TODO: Determine the behavior of the root endpoint.
#  Usually it will just be a testing point to see if the app is working.
@blueprint_main.route(EP_ROOT, methods=["GET"])
def root():
    """Root application entry point."""
    return RootResponse(message="Server is running.", ok=True)
