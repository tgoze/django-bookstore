from Store.Model.retail_order import RetailOrder
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error

class RetailOrderDao(AbcDao):

    def create(self, p_retail_order, p_cart_items):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            
            # Create an order in the retail order table of the DB
            args = (p_retail_order.total_price, p_retail_order.discount, 
                    p_retail_order.customer.customer_id, p_retail_order.shipping_address.address_id,
                    p_retail_order.billing_address.address_id, p_retail_order.card.card_id)
            cursor.callproc('createOrder', args)
            conn.commit()
            
            # Populate the association table with book data
            order_id = cursor.lastrowid
            for item in p_cart_items:
                args = (order_id, item.book_id, item.quantity_ordered)
                cursor.callproc('addBookToOrder', args)
                conn.commit()

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

    def get_byid(self):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
