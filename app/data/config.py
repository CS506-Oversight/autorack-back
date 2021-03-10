"""Configured instances for controlling the data."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

__all__ = ("db", "migrate")

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
