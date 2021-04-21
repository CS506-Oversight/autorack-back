import pint
from app.data import MenuModel, MenuController
from .measure_data import *
import json

#Get all orders
#Get menu items
#Make list of all ingredients from orders and amounts
#convert ingredients from total stock levls


__all__ = "InventoryController"

class InventoryController:

    @classmethod
    def getMenuItems(cls, user_id):
        menu = MenuController.get_menu(user_id=user_id)
        return menu


    @classmethod
    def updateInventory(cls, orders, user_id):
        """
        1. Grab the order (get the items purchase by menu_id and amount)
        2. Once you get the menu_ids then get the ingredients from that menu item
           (get ingredient id and measure)
        3. Merge the two into an array
        """
        ingredients_used = {}
        #print(user_id)
        #print(orders)
        menu = cls.getMenuItems(user_id)
        menu_dict = {}
        #create dictionary
        for menu_item in menu:
            menu_dict[menu_item['id']]=menu_item
        # print(menu_dict)
        for order_item in orders:
            #print(menu_item)
            ingredients = menu_dict[order_item['menu_id']]['ingredients']
            for ing in ingredients:
                print(ing)
                order_id = ing['id']
                unit_type = int(ing['measure']['type'])
                measure_name = ing['measure']['name']
                now_measure = float(ing['measure']['equivalentMetric']) * float(get_measurements(measure_name, unit_type))
                if order_id in ingredients_used:
                    ingredients_used[order_id] += (now_measure * int(order_item['amount']))
                else:
                    ingredients_used[order_id] = (now_measure * int(order_item['amount']))
            #print(ingredients)
        print(ingredients_used)


