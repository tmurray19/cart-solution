import typing

from . import abc
# Import OrderedDict to print out items in order they were entered
from collections import OrderedDict

# This is imported for an accurate day-to-day currency exchange
from forex_python.converter import CurrencyRates

class ShoppingCart(abc.ShoppingCart):
    def __init__(self, currency: str="EUR"):
        self._items = OrderedDict()
        # To store JSON information
        self._json = None
        # To store the currency of the Shopping Cart
        self._currency = currency

    # Accessor for json
    def get_json(self) -> dict:
        return self._json
    
    # Mutator for json
    def set_json(self, json: dict):
        self._json = json

    # Accessor for currency
    def get_currency(self) -> str:
        return self._currency

    # Mutator for currency
    def set_currency(self, currency: str):
        self._currency = currency

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
            # Modified code to handle products outside of price range
            price = self._get_product_price(item[0])
            # Only add to receipt, if price exists
            if price is not None:   
                # Convert price to desired price 
                price = self.convert_cost(price, self.get_currency())

                price *= item[1]
                total += price

                price_string = "%.2f" % price

                # lines.append(item[0] + " - " + str(item[1]) + ' - ' + price_string)
                lines.append(f'{item[0]} - {str(item[1])} - {price_string} {self.get_currency()}')
        lines.append(f'Total: {"%.2f" % total} {self.get_currency()}')
        return lines

    def _get_product_price(self, product_code: str) -> float:
        # Loading json should be optional
        if self.get_json() is not None:
            # Return product, or None if product doesn't exist in JSON
            if product_code in self.get_json():
                return self.get_json()[product_code]
            else:
                return None

        # Original functionality is currnently left in to not break existing functionality 
        price = None

        if product_code == 'apple':
            price = 1.0

        elif product_code == 'banana':
            price = 1.1

        elif product_code == 'kiwi':
            price = 3.0

        return price

    def convert_cost(self, price:float, desired:str) -> float:
        """
        Takes a specified price, gets the base currency from the shopping cart
        and converts the price to the destination 
        """
        #TODO: I am assuming this shop operates in Ireland, so all products are stored in Euro
        if self.get_currency() == "EUR":
            return price
    
        # Return regular price if currency not found
        return CurrencyRates().convert("EUR", desired, price) or price
        
