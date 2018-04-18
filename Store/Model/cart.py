from Store.Model.book import Book

class Cart():
    def __init__(self):
        self.user_id = None
        self.book = Book()
        self.quantity_ordered = None