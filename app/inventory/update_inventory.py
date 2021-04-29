import datetime
from decimal import Decimal

from sqlalchemy import and_

from app.data import MenuController, IngredientController, IngredientModel, RestockPurchaseController, \
    SupplierController, IngredientInProgressController, IngredientsInProgressModel

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
    def is_processing(cls, user_id: str, ingredient_id: str) -> bool:
        """
        Checks if an ingredient is already in the process of being restocked to
        prevent overstocking
        """
        return IngredientsInProgressModel.query.filter(
            and_(
                IngredientsInProgressModel.ingredient_id == ingredient_id,
                IngredientsInProgressModel.user_id == user_id
            )
        ).first() is not None

    @classmethod
    def restock(cls, user_id):
        # Threshold that current stock must drop below
        threshold = 0.15
        ingredients = IngredientController.get_ingredients(user_id=user_id)

        items_purchased = []
        updated_ingredients = []
        total_price = 0.0

        for ingredient in ingredients:
            if (ingredient["currentStockEquivalent"] <= ingredient["capacityEquivalent"] * threshold) \
                    and not cls.is_processing(user_id=user_id, ingredient_id=ingredient["id"]):
                print("RESTOCKING!!")
                # curr_stock = 0.0
                # curr_stock_equivalent = 0.0
                #
                # # Case in which stock and capacity units of ingredient are not the same
                # if ingredient["measure"]["name"] != ingredient["capacityMeasure"]["name"]:
                #     # Reset stock in the units used used by current stock
                #     curr_stock = float(ingredient["capacityEquivalent"]) / float(ingredient["measure"]["equivalentMetric"])
                #     # Reset stock equivalent in terms of the unit used for current stock
                #     curr_stock_equivalent = curr_stock * float(ingredient["measure"]["equivalentMetric"])
                # # Case in which stock and capacity units of ingredient are the same
                # else:
                #     curr_stock = ingredient["capacity"]
                #     curr_stock_equivalent = ingredient["capacityEquivalent"]
                #
                # updated_ingredients.append({
                #     "id": ingredient["id"],
                #     "currentStock": curr_stock,
                #     "measure": ingredient["measure"],
                #     "name": ingredient["name"],
                #     "capacity": ingredient["capacity"],
                #     "capacityEquivalent": ingredient["capacityEquivalent"],
                #     "capacityMeasure": ingredient["capacityMeasure"],
                #     "currentStockEquivalent": curr_stock_equivalent
                # })

                # Gets the randomized price from the supplier db
                ingredient_price = SupplierController.get_ingredient_price(ingredient["id"])

                max_amount_equivalent = ingredient["capacityEquivalent"]
                curr_equivalent = ingredient["currentStockEquivalent"]
                # Gets the difference between the capacity (g or l) and current stock equivalent (g or l)
                stock_diff = max_amount_equivalent - curr_equivalent

                # Calculates how much in stock units needs to be purchased for an ingredient
                quantity_purchased = round(stock_diff / ingredient["measure"]["equivalentMetric"])

                amount_in_progress_decimal = float(stock_diff)/float(max_amount_equivalent)
                amount_in_progress_percentage = amount_in_progress_decimal * float(100)

                IngredientInProgressController.add_ingredients_in_progress(
                    user_id=user_id,
                    name=ingredient["name"],
                    ingredient_id=ingredient["id"],
                    amount_in_progress=quantity_purchased,
                    amount_in_progress_percentage=amount_in_progress_percentage
                )

                # Calculates price while preserving precision
                calculated_price = round(Decimal(str(float(ingredient_price) * float(int(quantity_purchased)))), 2)
                total_price += float(calculated_price)

                items_purchased.append({"description": ingredient["name"], "unitPrice": ingredient_price,
                                        "quantity": int(quantity_purchased)})
            else:
                print('NOT RESTOCKING')

        # IngredientController.upsert_ingredients(user_id=user_id, payload=updated_ingredients)
        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")

        if items_purchased:
            actual_total_price = round(Decimal(str(total_price)), 2)
            # All new restock purchases start out with a status of 'processing'
            RestockPurchaseController.add_restock_purchase(status="processing", total_price=actual_total_price,
                                                           purchase_date=formatted_date, purchase_type="Auto",
                                                           items_purchased=items_purchased, user_id=user_id
                                                           )
