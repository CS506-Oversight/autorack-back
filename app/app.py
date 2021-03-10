"""Implementations for app construction."""
import os
import sys
from typing import TypeVar

from dotenv import load_dotenv
from flask import Flask, Response

from .data import db, migrate
from .response import ResponseBase
from .routes import blueprint_main

__all__ = ("create_app",)

# Load environment variables defined in `.env`
load_dotenv()

T = TypeVar("T", bound=ResponseBase)


class App(Flask):
    """
    Custom Flask app class.

    The purpose of this is to override or add some implementations to the Flask app behavior.
    """

    def make_response(self, response: T) -> Response:
        # Only accepts response instance that inherits `ResponseBase`
        if isinstance(response, ResponseBase):
            # Convert `response` to Flask response object
            response = response.to_flask_response()

        # Execute `make_response()` of the super class and return it
        return super().make_response(response)


def create_app() -> Flask:
    """Creates a Flask app and return it."""
    app: Flask = App(__name__)

    # Connect & Migrate database
    # TODO: pylint disable statement to-be-removed after fix:
    #  not with walrus https://github.com/PyCQA/pylint/issues/3249
    # pylint: disable=superfluous-parens
    if not (sql_alchemy_uri := os.getenv("SQLALCHEMY_DATABASE_URI")):
        print(
            "Specify the database connection string for PostgreSQL as `SQLALCHEMY_DATABASE_URI` "
            "in the environment variables."
        )
        sys.exit(1)

    app.config["SQLALCHEMY_DATABASE_URI"] = sql_alchemy_uri
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    app.register_blueprint(blueprint_main)

    return app
