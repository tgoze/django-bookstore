from Store.Model.book_order import BookOrder
from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error

class BookOrderDao(AbcDao):

    def create(self, parameter_list):
        raise NotImplementedError
    def get_all(self, parameter_list):
        raise NotImplementedError
    def get_byid(self, order_id):
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            bookorders = []
            args = [order_id]
            # Calls the stored procedure
            cursor.callproc('getBooksOnOrder', args)         
            bdao = BookDao()
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    bookorder = BookOrder()
                    bookorder.order_id = x[0]
                    bookorder.book = bdao.get_byid(x[1])
                    bookorder.quantity = x[2]
                    bookorder.price = x[3]
                    bookorder.discount = x[4]
                    bookorders.append(bookorder)
        
            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return bookorders

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError