<<<<<<< HEAD
from author_dao import AuthorDao
from author import Author

if __name__ == '__main__':
    
    author_dao = AuthorDao()
    
    # author = Author()
    # author.author_id = 11
    # author.first_name = "George"
    # author.last_name = "Smith"
    # author_dao.update(author)
=======
from book_dao import BookDao
from genre_dao import GenreDao
from inventory_dao import InventoryDao
from inventory import Inventory

if __name__ == '__main__':
    
    inv = InventoryDao()
    for x in inv.get_all():
        print(x.book_id,x.quantity_on_hand,x.quantity_ordered,x.cost,x.retail_price)
    
>>>>>>> origin/kara_line

    # for x in author_dao.get_all():
    #     print(x.author_id, x.first_name, x.last_name)

    author_dao.delete(11)