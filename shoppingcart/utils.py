# utils.py

import json

def open_json(location) -> dict:
    """
    Looks for a JSON file at the given path location, opens the file, and returns the loaded json data 
    """
    f = open(location)
    data = json.load(f)
    f.close()
    return data
