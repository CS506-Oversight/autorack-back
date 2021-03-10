"""Main routes."""
from flask import Blueprint, request

from app.response import RootResponse, SimpleAddResponse, MealAddedResponse, MealControlFailedResponse
from app.data import MealController

from .path import EP_ROOT, EP_ADD, EP_DATA

__all__ = ("blueprint_main",)

blueprint_main: Blueprint = Blueprint("main", __name__)


# TODO: Determine the behavior of the root endpoint.
#  Usually it will just be a testing point to see if the app is working.
@blueprint_main.route(EP_ROOT, methods=["GET"])
def root():
    """Root application entry point."""
    return RootResponse(message="I am a dummy to be voided in the near future, poor me.", ok=True)


# TODO: [Example] endpoint: perform a simple addition and return it
@blueprint_main.route(EP_ADD, methods=["GET"])
def simple_add():
    """Endpoint for performing a single calculation."""
    arg1 = request.args.get("arg1", type=int)
    arg2 = request.args.get("arg2", type=int)

    return SimpleAddResponse(result=arg1 + arg2)


# TODO: [Example] endpoint: add a dummy meal and return it
@blueprint_main.route(EP_DATA, methods=["GET"])
def data_test():
    """Endpoint for testing data connection and manipulations."""
    # Insert a dummy data
    # [!] Name arguments using `camelCase`
    meal_name = request.args.get("mealName")

    # Add a dummy meal
    meal_added = MealController.add_meal(meal_name)

    # Returns failure response if the meal is not added
    if not meal_added:
        # [!] If possible, make `add_meal` returns an enum representing the failure reason,
        # and send the error message according to the failure reason instead.
        return MealControlFailedResponse(message=f"Failed to add a meal with name: {meal_name}")

    # Get the dummy meal we just added
    meal = MealController.get_meal(meal_name)

    # Returns failure response if the meal is not found
    if not meal:
        # [!] Although this is not possible under this logic,
        # we must handle the case where meal is not available once we've separate the logic.
        return MealControlFailedResponse(message=f"Meal with name {meal_name} not found.")

    # Return a response indicating that a meal has been added
    return MealAddedResponse(meal)
