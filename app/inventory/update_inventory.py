from app.data import MenuController, IngredientController, IngredientModel, RestockPurchaseController, \
    SupplierController
import datetime
from .measure_data import *
import json

# Get all orders
# Get menu items
# Make list of all ingredients from orders and amounts
# convert ingredients from total stock levels

__all__ = "InventoryController"


class InventoryController:
    @classmethod
    def get_menu_items(cls, user_id):
        return MenuController.get_menu(user_id=user_id)

    @classmethod
    def get_ingredients(cls, user_id):
        return IngredientController.get_ingredients(user_id=user_id)

    @classmethod
    def update_inventory(cls, orders, user_id):
        """
        1. Grab the order (get the items purchase by menu_id and amount)
        2. Once you get the menu_ids then get the ingredients from that menu item
           (get ingredient id and measure)
        3. Merge the two into an array
        """
        menu = cls.get_menu_items(user_id)
        ingredients = cls.get_ingredients(user_id)

        menu_dict = {}
        ingredients_used = {}

        for menu_item in menu:
            menu_dict[menu_item['id']] = menu_item

        for order_item in orders:
            menu_ingredients = menu_dict[order_item['menu_id']]['ingredients']
            for ingredient in menu_ingredients:
                ingredient_id = ingredient['id']
                now_measure = ingredient["currentStockEquivalent"]

                if ingredient_id in ingredients_used:
                    ingredients_used[ingredient_id] += (now_measure * int(order_item['amount']))
                else:
                    ingredients_used[ingredient_id] = (now_measure * int(order_item['amount']))

        updated_ingredients = []

        for ingredient_id in ingredients_used:
            actual_ingredient = IngredientModel.query.filter_by(ingredient_id=ingredient_id).first()

            ingredient = actual_ingredient.to_dict()

            curr_stock_equivalent = float(ingredient["currentStockEquivalent"])
            measure = ingredient["measure"]
            amount_used = ingredients_used[ingredient_id]

            updated_stock_equivalent = curr_stock_equivalent - amount_used
            updated_stock = float(updated_stock_equivalent) / float(measure["equivalentMetric"])

            updated_ingredients.append({
                "id": ingredient_id,
                "currentStock": updated_stock,
                "measure": measure,
                "name": ingredient["name"],
                "capacity": ingredient["capacity"],
                "capacityEquivalent": ingredient["capacityEquivalent"],
                "capacityMeasure": ingredient["capacityMeasure"],
                "currentStockEquivalent": updated_stock_equivalent
            })

        IngredientController.upsert_ingredients(user_id=user_id, payload=updated_ingredients)
        cls.restock(user_id=user_id)

    @classmethod
    def restock(cls, user_id):
        # Restock Limit 15%
        limit = 0.15
        ingredients = IngredientController.get_ingredients(user_id=user_id)

        items_purchased = []
        updated_ingredients = []
        total_price = 0.0

        for ingredient in ingredients:
            if ingredient["currentStock"] < ingredient["capacity"] * limit:
                updated_ingredients.append({
                    "id": ingredient["id"],
                    "currentStock": ingredient["capacity"],
                    "measure": ingredient["measure"],
                    "name": ingredient["name"],
                    "capacity": ingredient["capacity"],
                    "capacityEquivalent": ingredient["capacityEquivalent"],
                    "capacityMeasure": ingredient["capacityMeasure"],
                    "currentStockEquivalent": ingredient["capacityEquivalent"]
                })

                # calculate price from supplier database
                ingredient_price = SupplierController.get_ingredient_price(ingredient["id"])

                max_amount = ingredient["capacityEquivalent"]
                curr_equivalent = ingredient["currentStockEquivalent"]
                stock_diff = max_amount - curr_equivalent
                # print(f'STOCK DIFF: {stock_diff}\n')

                quantity_purchased = round(stock_diff / ingredient["measure"]["equivalentMetric"])
                # print(f'QUANTITY PURCHASED: {quantity_purchased}\n')

                total_price += (float(ingredient_price) * float(int(quantity_purchased)))
                # print(f'TOTAL PRICE: {total_price}\n')

                items_purchased.append({"description": ingredient["name"], "unitPrice": ingredient_price,
                                        "quantity": int(quantity_purchased)})
                # print(f'ITEMS PURCHASED: {items_purchased}\n')

        IngredientController.upsert_ingredients(user_id=user_id, payload=updated_ingredients)
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")

        if items_purchased:
            RestockPurchaseController.add_restock_purchase(status="processing", total_price=total_price,
                                                           purchase_date=formatted_date, purchase_type="Auto",
                                                           items_purchased=items_purchased, user_id=user_id
                                                           )
