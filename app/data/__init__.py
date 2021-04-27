"""Data models and the related controller."""
from .config import db, migrate
from .user_data import UserModel, UserController
from .restock_purchase_data import RestockPurchaseModel, RestockPurchaseController
from .ingredient_data import IngredientModel, IngredientController
from .menu_data import MenuModel, MenuController
