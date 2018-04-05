from book_dao import BookDao
from genre_dao import GenreDao
from inventory_dao import InventoryDao
from inventory import Inventory

if __name__ == '__main__':
    
    book_dao = BookDao()
    for x in book_dao.get_all():
        print(x.title)