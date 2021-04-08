"""Data models and the related controller."""
from .config import db, migrate
from .meal import MealModel, MealController
from .user import UserModel, UserController
from .restock_purchase import RestockPurchaseModel, RestockPurchaseController
