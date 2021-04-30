import datetime
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.data.base import UtilController
from app.data import MenuController, IngredientController, IngredientModel, RestockPurchaseController, \
    SupplierController, IngredientInProgressController, IngredientsInProgressModel, RestockPurchaseModel

__all__ = "InventoryController"


class InventoryController(UtilController):
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

        total_price = 0.0

        for ingredient in ingredients:
            if (ingredient["currentStockEquivalent"] <= ingredient["capacityEquivalent"] * threshold) \
                    and not cls.is_processing(user_id=user_id, ingredient_id=ingredient["id"]):
                print("RESTOCKING!!")

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

        current_day = datetime.date.today()
        formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")

        if items_purchased:
            actual_total_price = round(Decimal(str(total_price)), 2)
            # All new restock purchases start out with a status of 'processing'
            RestockPurchaseController.add_restock_purchase(status="processing", total_price=actual_total_price,
                                                           purchase_date=formatted_date, purchase_type="Auto",
                                                           items_purchased=items_purchased, user_id=user_id
                                                           )

    @classmethod
    def fulfill_inventory(cls, user_id):
        processing_purchases = RestockPurchaseModel.query.filter(
            and_(
                RestockPurchaseModel.user_id == user_id,
                RestockPurchaseModel.status == "processing"
            )
        ).all()

        session: Session = cls.get_session()

        for purchase in processing_purchases:
            session.query(RestockPurchaseModel).filter(
                and_(
                    RestockPurchaseModel.user_id == user_id,
                    RestockPurchaseModel.purchase_id == purchase.purchase_id
                )
            ).update({"status": "completed"})

            session.commit()

        ingredients_in_progress = IngredientsInProgressModel.query.filter_by(user_id=user_id).all()

        updated_ingredients = []

        for ingredient in ingredients_in_progress:
            ingredient_info = IngredientModel.query.filter(
                and_(
                    IngredientModel.user_id == user_id,
                    IngredientModel.ingredient_id == ingredient.ingredient_id
                )
            ).first()

            ingredient_info_dict = ingredient_info.to_dict()

            in_progress_equivalent = float(ingredient.amount_in_progress) * float(
                ingredient_info_dict["measure"]["equivalentMetric"]
            )

            new_stock = float(ingredient.amount_in_progress) + float(ingredient_info_dict["currentStock"])
            new_equivalent = in_progress_equivalent + float(ingredient_info_dict["currentStockEquivalent"])

            updated_ingredients.append({
                "id": ingredient_info_dict["id"],
                "currentStock": new_stock,
                "measure": ingredient_info_dict["measure"],
                "name": ingredient_info_dict["name"],
                "capacity": ingredient_info_dict["capacity"],
                "capacityEquivalent": ingredient_info_dict["capacityEquivalent"],
                "capacityMeasure": ingredient_info_dict["capacityMeasure"],
                "currentStockEquivalent": new_equivalent
            })

            IngredientInProgressController.delete_ingredients_in_progress(user_id=user_id, ingredient_id=ingredient_info_dict["id"])

        IngredientController.upsert_ingredients(user_id=user_id, payload=updated_ingredients)
