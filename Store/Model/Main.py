
from book_dao import BookDao
from genre_dao import GenreDao
from inventory_dao import InventoryDao
from inventory import Inventory
from user_dao import UserDao
from user import User
from customer_address_dao import CustomerAddressDao
from customer_address import CustomerAddress
from payment_info import PaymentInfo
from payment_info_dao import PaymentInfoDao

if __name__ == '__main__':
    settings.configure(DEBUG=True)
    p = PaymentInfo()
    pdao = PaymentInfoDao()
    p.customer_id = 1
  
    for x in pdao.get_all(p):
        print(x.card_number)

    
    
  
    
    

