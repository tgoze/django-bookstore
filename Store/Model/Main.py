from book_dao import BookDao
from genre_dao import GenreDao
from inventory_dao import InventoryDao
from inventory import Inventory

if __name__ == '__main__':
    
    inv = InventoryDao()
    for x in inv.get_all():
        print(x.book_id,x.quantity_on_hand,x.quantity_ordered,x.cost,x.retail_price)
    

