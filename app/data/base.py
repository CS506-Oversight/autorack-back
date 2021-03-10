"""Base classes of the data models and the data controllers."""
from abc import ABC
from typing import Type, TypeVar

from sqlalchemy.orm import Query, Session

from .config import db

__all__ = ("Controller",)


T = TypeVar("T", bound=db.Model)


class Controller(ABC):
    """
    Base class of a data controller.

    Class variable `model`, or the class method `get_model()`
    should be overridden for getting the actual model of this controller.
    """

    model: Type[T] = None

    @classmethod
    def get_session(cls) -> Session:
        """Get the current database session."""
        # The reason of having this is because that
        # we might want to generate sessions if we decide to run the app asuynchronously.
        # Separating the process of getting a database session allows us
        # to potentially generate sessions without changing too much in code.
        return db.session

    @classmethod
    def get_model(cls) -> Type[T]:
        """Get the model class of this data controller."""
        # Sometimes we might want do dynamically obtain the data model we want.
        # Having this method allows us to either override this method to get the model,
        # or statically get the model class to perform query.
        # This also allows us to access the auto-complete of `model.query` by type-hinting (using `get_query()`).
        return cls.model

    @classmethod
    def get_query(cls) -> Query:
        """
        Get the query variable of the model class of this controller.

        Query variable to be returned is determined by what ``get_model()`` returns.
        """
        return cls.get_model().query
