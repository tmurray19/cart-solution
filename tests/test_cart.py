from shoppingcart.cart import ShoppingCart


def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 1 - €1.00"


def test_add_item_with_multiple_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 2)

    receipt = cart.print_receipt()

    assert receipt[0] == "apple - 2 - €2.00"


def test_add_different_items():
    cart = ShoppingCart()
    cart.add_item("banana", 1)
    cart.add_item("kiwi", 1)

    receipt = cart.print_receipt()

    assert receipt[0] == "banana - 1 - €1.10"
    assert receipt[1] == "kiwi - 1 - €3.00"

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

    assert receipt[0] == "banana - 3 - €3.30"
    assert receipt[1] == "kiwi - 99 - €297.00"
    assert receipt[2] == "apple - 3 - €3.00"