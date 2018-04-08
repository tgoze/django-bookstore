
from book_dao import BookDao
from genre_dao import GenreDao
from inventory_dao import InventoryDao
from inventory import Inventory
from user_dao import UserDao
from user import User
from customer_address_dao import CustomerAddressDao
from customer_address import CustomerAddress



if __name__ == '__main__':
    #settings.configure(DEBUG=True)
    c = CustomerAddress()
    cdao = CustomerAddressDao()
    #c.address_id=1
    c.street = '234 Main Street'
    c.city = 'Troy'
    c.state_code='MO'
    c.zip_code=65616
    c.customer_id=1
    c.address_type='shipping'
    cdao.create(c)
    
    
  
    
    

