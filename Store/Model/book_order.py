from Store.Model.retail_order import RetailOrder
from Store.Model.book import Book


class BookOrder:
    def __init__(self):
        self.order_id = RetailOrder()
        self.book = Book()
        self.quantity = None
        self.price = None
        self.discount = None