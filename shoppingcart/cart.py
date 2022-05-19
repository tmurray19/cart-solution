import typing

from . import abc
# Import OrderedDict to print out items in order they were entered
from collections import OrderedDict

# This is imported for an accurate day-to-day currency exchange
from forex_python.converter import CurrencyRates

class ShoppingCart(abc.ShoppingCart):
    def __init__(self, currency: str="EUR"):
        """
        Create a new Shopping Cart instance

        items -> List of products in a given Cart
        currency -> ISO Tag for currency [EUR=euro, USD=American Dollars, GBP=UK Pounds, etxc.]
        json -> For storing any loaded json 
        """
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
 
    ## Adding accessor and mutator for existing private variable
    # Accessor for items
    def get_items(self) -> OrderedDict:
        return self._items
    
    # Mutator for items
    def set_items(self, items: OrderedDict):
        self._items = items

    
    def add_item(self, product_code: str, quantity: int):
        """
        Attempts to add a product to the list of items. If the item doesnt exist, it adds it with the specified quantity
        Otherwise, it adds the quantity to the existing product

        product_code: str -> The product code as defined in the JSON, or the default price list in the _get_product_price() function
        quantity: int -> The amount to add to the shopping cart
        """
        if product_code not in self.get_items():
            self.get_items()[product_code] = quantity
        else:
            # Removed a line
            self.get_items()[product_code] += quantity

    def print_receipt(self) -> typing.List[str]:
        """
        Iterates through the list of items in the shopping cart, and returns the data as a formatted list, along with the total at the end
        """
        lines = []

        # Defining total variable to add to in for loop
        total = 0

        # Unpacking iteratbles for readability
        for product, quantity in self._items.items():
            # Modified code to handle products outside of price range
            price = self._get_product_price(product)
            # Only add to receipt, if price exists
            if price is not None:   
                # Convert price to desired price 
                price = self.convert_cost(price, self.get_currency())

                price *= quantity
                total += price

                lines.append(f'{product} - {quantity} - {"%.2f" % price} {self.get_currency()}')
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

        price: float -> Base cost that you want to convert
        desired: str -> ISO Currency code you want to convert the price into 
        """
        #TODO: I am assuming this shop operates in Ireland, so all products are stored in Euro
        if self.get_currency() == "EUR":
            return price
    
        # Return regular price if currency not found
        return CurrencyRates().convert("EUR", desired, price) or price
        
