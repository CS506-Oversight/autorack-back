"""Data model and controller for users."""
import datetime
from typing import Optional

from sqlalchemy.orm import Session

from .base import Controller
from .config import db

__all__ = ("UserModel", "UserController")


class UserModel(db.Model):
    """Data model for users."""

    # No model-level methods to add yet
    # pylint: disable=too-few-public-methods

    __tablename__ = "user"

    user_id = db.Column(db.String(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self, user_id: str, first_name: str, last_name: str, created_at: datetime, email: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.email = email

    def __repr__(self):
        return f"<User {self.user_id}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.first_name,
        }


class UserController(Controller):
    """Controller for users."""

    model = UserModel

    @classmethod
    def add_user(cls, user_id: str, first_name: str, last_name: str, created_at: datetime, email: str) -> bool:
        """
        Add a user and return when the user is added.
        """
        session: Session = cls.get_session()

        model = UserModel(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            created_at=created_at,
            email=email
        )

        session.add(model)
        session.commit()

        return True

    @classmethod
    def get_user(cls, user_id: str) -> UserModel:
        """Gets the user with ``user_id``."""
        return cls.get_query().filter_by(user_id=user_id).first()
