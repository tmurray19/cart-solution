from shoppingcart.cart import ShoppingCart
from shoppingcart.json_db import JsonDB
from forex_python.converter import CurrencyRates

def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 1 - 1.00 EUR"


def test_add_item_with_multiple_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 2)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 2 - 2.00 EUR"


def test_add_different_items():
    cart = ShoppingCart()
    cart.add_item("banana", 1)
    cart.add_item("kiwi", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 1 - 1.10 EUR"
    assert receipt[1] == "kiwi - 1 - 3.00 EUR"

def test_printed_in_order():
    """
    Shows that banana was added first, and comes out in the receipt list first
    """
    cart = ShoppingCart()
    cart.add_item("banana", 1)
    cart.add_item("kiwi", 99)
    cart.add_item("banana", 1)
    cart.add_item("apple", 3)
    cart.add_item("banana", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 3 - 3.30 EUR"
    assert receipt[1] == "kiwi - 99 - 297.00 EUR"
    assert receipt[2] == "apple - 3 - 3.00 EUR"

def test_total():
    """
    Shows that the total amount has been appended to the receipt
    """
    cart = ShoppingCart()
    cart.add_item("banana", 1)


    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 1 - 1.10 EUR"
    assert receipt[1] == "Total: 1.10 EUR"

def test_total_multiple():
    """
    Shows that the total amount has been appended to the end of the receipt
    """
    cart = ShoppingCart()
    cart.add_item("banana", 1)
    cart.add_item("apple", 3)
    cart.add_item("kiwi", 2)
    cart.add_item("banana", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 2 - 2.20 EUR"
    # Check last element of list
    assert receipt[-1] == "Total: 11.20 EUR"

def test_empty():
    """
    Test to show that total can handle an empty cart
    """
    cart = ShoppingCart()

    assert cart.print_receipt()[0] == "Total: 0.00 EUR"

def test_read_from_json():
    """
    Test to show that JSON can be read from, and it overwrites any existing price
    """

    # Show a baseline receipt with the default banana price
    cart = ShoppingCart()
    jsondb = JsonDB()
    cart.add_item("banana", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 1 - 1.10 EUR"     
 
    # Create a new ShoppingCart instance 
    cart = ShoppingCart()

    # Open and set JSON 
    cart.set_json(jsondb.open_db('tests\sample.json'))

    # Add an item to cart
    cart.add_item("banana", 1)
    receipt = cart.print_receipt()
    
    # Showing that there has been a price change, and that the shopping cart is reading the updated price as defined in the JSON
    assert receipt[0] == "banana - 1 - 1.50 EUR"

def test_read_empty():
    """
    Test to show that system can handle a product that doesn't exist
    """

    cart = ShoppingCart()

    # Adding item out of price list
    cart.add_item("shoes", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "Total: 0.00 EUR"

def test_read_empty_json():
    """
    Test to show that system can handle a product that doesn't exist in the JSON
    """

    cart = ShoppingCart()
    jsondb = JsonDB()
    cart.set_json(jsondb.open_db('tests\sample.json'))

    # Adding item out of JSON price list
    cart.add_item("shoes", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "Total: 0.00 EUR"

def test_currency_changer_set():

    """
    Test that the currency of a cart can be set and changed
    """
    cart = ShoppingCart()

    assert cart.get_currency() == "EUR"
    cart.set_currency("USD")
    assert cart.get_currency() == "USD"

    # Test that it can be set on startup
    cart = ShoppingCart("USD")
    assert cart.get_currency() == "USD"

def test_currency_exchange_end_to_end():
    """
    Test that receipt can output price in requested currency
    """
    cart = ShoppingCart(currency="USD")
    
    # Add Items
    cart.add_item("banana", 1)
    cart.add_item("kiwi", 1)

    receipt = cart.print_receipt()

    c = CurrencyRates()

    assert receipt[0] == f'banana - 1 - {"%.2f" % c.convert(base_cur="EUR", dest_cur="USD", amount=1.10)} USD'
    assert receipt[1] == f'kiwi - 1 - {"%.2f" % c.convert("EUR", "USD", 3.00)} USD'

def test_json_end_to_end():
    """
    Test functions for interfacing with JSON database
    """
    c =  JsonDB()
    c.open_db('tests\sample.json')

    # Test Product can be added
    c.add_product({"grapes": 1})
    assert c.get_product("grapes") == 1

    # Test product 
    c.add_product({"peaches": 3.5})
    assert c.get_product("peaches") == 3.5

    # Test removing product
    c.add_product({"cars": 2.0})
    assert c.get_product("cars") == 2.0

    c.remove_product("cars")
    assert c.get_product("cars") == None

    # Test update product
    c.update_product("grapes", 4.0)
    assert c.get_product("grapes") == 4.0

    # Test that all changes have been made correctly
    assert c.open_db('tests\sample.json') == {"apple": 1.0, "banana": 1.5, "kiwi": 3.0, "grapes": 4.0, "peaches": 3.5}


def test_json_further():
    """
    Further tests for JSON functionality, making sure code can handle unexpected inputs
    """

    c =  JsonDB()
    c.open_db('tests\sample.json')

    # Test None Value
    c.add_product({"bananas": None})
    assert c.get_product("bananas") == None

    # Test String value
    c.add_product({"peaches": "3.5"})
    assert c.get_product("peaches") == "3.5"

    # Test that ShoppingCart can handle string value
    cart = ShoppingCart()
    cart.set_json(c.get_json())

    # Peaches is handled correctly
    cart.add_item("peaches", 1)
    # Banana is added, but ignored in print receipt
    cart.add_item("bananas", 1)

    assert cart.print_receipt()[0] == "peaches - 1 - 3.50 EUR"
    assert cart.print_receipt()[1] == "Total: 3.50 EUR"

    # Test removing non existing value
    c.remove_product("dragonfruit")
    assert c.get_product("dragonfruit") == None

    # Test update product - product doesn't exist in system
    c.update_product("lychee", 4.0)
    assert c.get_product("lychee") == None

    # Test that all changes have been made correctly
    assert c.open_db('tests\sample.json') == {"apple": 1.0, "banana": 1.5, "kiwi": 3.0, "grapes": 4.0, "peaches": "3.5", "bananas": None}

    # Remove null bananas record from JSON file
    c.remove_product('bananas')