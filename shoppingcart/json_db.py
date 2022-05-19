# json_db.py

import json

from . import abc

class JsonDB(abc.DatabaseAccess):
    """
    Implementation of DatabaseAccess abstract class
    """

    def __init__(self):
        self._json = dict()
        self._json_loc = None

    # Accessors and Mutators 
    def set_json(self, json: dict):
        self._json = json

    def get_json(self) -> dict:
        return self._json

    def set_json_loc(self, json_loc: str):
        self._json_loc = json_loc

    def get_json_loc(self) -> dict:
        return self._json_loc

    def open_db(self, location: str) -> dict:
        """
        Looks for a JSON file at the given path location, opens the file, and returns the loaded json data

        location: str -> The Path to the file to open and read 
        """
        f = open(location)
        data = json.load(f)
        f.close()

        print(data)

        # Set variables for class
        self.set_json(data)
        self.set_json_loc(location)

        return data
 
    # Private variable to save changes made to file as they are made to loaded json object
    def _save_json_changes(self):
        """
        Saves changes made to JSON - Internal function
        """
        with open(self.get_json_loc(), 'w') as file:
            json.dump(self.get_json(), file)
        file.close()
  
    def add_product(self, product: dict):
        """
        Adds a product to the JSON

        product: dict -> The product to be added to the JSON.
        """
        self.get_json().update(product)
        self._save_json_changes()


    def remove_product(self, product_id: str):
        """
        Remove a specified product from the JSON

        product_id: str -> The ID of the product you want removed from the JSON
        """
        self.get_json().pop(product_id)
        self._save_json_changes()

    def get_product(self, product_id: str) -> float:
        """
        Return a specified product
        """
        try:
            return self.get_json()[product_id]
        except KeyError:
            return None

    
    def update_product(self, product_id: str, update: float):
        """
        Update a specified product id with the new cost

        product_id: str -> The product ID the system needs to look for
        update: float -> The new price of the product
        """
        self.get_json()[product_id] = update
        self._save_json_changes()
