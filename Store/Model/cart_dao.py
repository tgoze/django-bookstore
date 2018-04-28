from Store.Model.abc_dao import AbcDao
from Store.Model.cart import Cart
from Store.Model.inventory import Inventory

from Store.Model.dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error

class CartDao(AbcDao):

    def create(self, p_cart):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_cart.book.book_id, p_cart.user_id, p_cart.quantity_ordered)
            cursor.callproc('addToCart', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)        
    
    def get_byid(self):
        raise NotImplementedError

    def get_all(self, p_user_id):
        cart_items = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            args = (p_user_id,)
            cursor.callproc('getCartByUserID', args)         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for cart_row in result.fetchall():
                    cart = Cart()
                    cart.book.book_id = cart_row[0]
                    cart.user_id = cart_row[1]
                    cart.quantity_ordered = cart_row[2]                    
                    cart.book.ISBN13 = cart_row[3]
                    cart.book.ISBN10 = cart_row[4]
                    cart.book.title = cart_row[5]
                    cart.book.copyRightDate = cart_row[6]
                    cart.book.bookType = cart_row[7]
                    cart.book.edition = cart_row[8]
                    cart.book.numberOfPages = cart_row[9]
                    cart.book.genre.genre_id = cart_row[10]
                    cart.book.author.author_id = cart_row[11]
                    cart.book.publisher.publisher_id = cart_row[12]
                    cart.book.inventory.quantity_on_hand = cart_row[13]
                    cart.book.inventory.retail_price = cart_row[14]
                    cart_items.append(cart)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return cart_items

    def update(self, p_cart):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_cart.book.book_id, p_cart.user_id, p_cart.quantity_ordered)
            cursor.callproc('updateCart', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

    def delete(self):
        raise NotImplementedError

    def delete_from_cart(self, p_book_id, p_user_id):    
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args= (p_book_id, p_user_id)
            cursor.callproc('deleteFromCart', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
