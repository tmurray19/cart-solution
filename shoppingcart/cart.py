import typing

from . import abc
# Import OrderedDict to print out items in order they were entered
from collections import OrderedDict

class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = OrderedDict()
        # To store JSON information
        self._json = None

    # Accessor for json
    def get_json(self) -> dict:
        return self._json
    
    # Mutator for json
    def set_json(self, json: dict):
        self._json = json


    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

    def print_receipt(self) -> typing.List[str]:
        lines = []

        # Defining total variable to add to in for loop
        total = 0

        for item in self._items.items():
            price = self._get_product_price(item[0]) * item[1]
            total += price

            price_string = "€%.2f" % price

            lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string)
        lines.append(f'Total: €{"%.2f" % total}')
        return lines

    def _get_product_price(self, product_code: str) -> float:
        # Loading json should be optional
        if self.get_json() is not None:
            # Return product, or None if product doesn't exist in JSON
            if product_code in self.get_json():
                return self.get_json()[product_code]
            else:
                return None

        price = 0.0

        if product_code == 'apple':
            price = 1.0

        elif product_code == 'banana':
            price = 1.1

        elif product_code == 'kiwi':
            price = 3.0

        return price
