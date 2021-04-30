"""Blueprints for the Flask app."""
from .main import blueprint_main
from .user_routes import blueprint_user
from .menu_routes import blueprint_menu
from .restock_purchase_routes import blueprint_restock_purchase
from .ingredient_routes import blueprint_ingredient
from .order_routes import blueprint_order
from .inventory_routes import blueprint_inventory
