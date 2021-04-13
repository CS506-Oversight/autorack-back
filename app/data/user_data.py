"""Data model and controller for users."""
import datetime

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


class UserController(Controller):
    """Controller for users."""

    model = UserModel

    @classmethod
    def add_user(cls, user_id: str, first_name: str, last_name: str, created_at: datetime, email: str) -> bool:
        """
        Add a user and return if the user is added or not.

        If ``email`` already exists
        this directly returns ``False`` without performing any additional actions.
        """
        email_check = cls.get_query().filter_by(email=email).first() is not None
        user_id_check = cls.get_query().filter_by(user_id=user_id).first() is not None
        
        if email_check or user_id_check:
            return False

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

    @classmethod
    def delete_user(cls, user_id: str) -> UserModel:
        """
        Deletes the user with ``user_id``.

        TODO: Before deleting a user, there must be extensive checks
        (e.g. are there still any pending restock purchases, etc.).

        A user's restock purchases preferences should automatically
        be set to manual to ensure that no other purchases are made at
        the end of the day.
        """
        user = cls.get_user(user_id=user_id)

        if not user:
            return user

        session: Session = cls.get_session()

        session.delete(user)
        session.commit()

        return user

    @classmethod
    def update_user(cls, user_id: str) -> UserModel:
        """TODO: Update the user with ``user_id``."""
        pass

