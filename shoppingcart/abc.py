
import abc
import typing


class ShoppingCart(abc.ABC):

    @abc.abstractmethod
    def add_item(self, product_code: str, quantity: int):
        pass

    @abc.abstractmethod
    def print_receipt(self) -> typing.List[str]:
        pass

class DatabaseAccess(abc.ABC):
    """
    This is an abstract class to be extended to attempt to create a unified db connection service
    """
    @abc.abstractmethod
    def open_db(self, location: str):
        pass
    
    @abc.abstractmethod
    def add_product(self, product: dict):
        pass

    @abc.abstractmethod
    def remove_product(self, product_id: str):
        pass

    @abc.abstractmethod
    def update_product(self, product_id: str, update: float):
        pass

    @abc.abstractmethod
    def get_product(self, product_id: str) -> float:
        pass

