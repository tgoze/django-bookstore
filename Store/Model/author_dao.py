from Store.Model.author import Author
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error

class AuthorDao(AbcDao):

    def create(self, p_author):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_author.first_name, p_author.last_name)
            cursor.callproc('createAuthor', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        
    
    def get_all(self):
        try:
            authors = []
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            cursor.callproc('getAllAuthors')         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                
                # This loop iterates through the rows in each resultset
                for author_row in result.fetchall():
                    
                    author = Author()
                    author.author_id = author_row[0]
                    author.first_name = author_row[1]
                    author.last_name = author_row[2]                    
                    authors.append(author)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return authors


    def get_byid(self, author_id):
        try:
            author = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [author_id]
            # Calls the stored procedure
            cursor.callproc('getAuthorByAuthorID', args)         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                
                # This loop iterates through the rows in each resultset
                for author_row in result.fetchall():
                    
                    author = Author()
                    author.author_id = author_row[0]
                    author.first_name = author_row[1]
                    author.last_name = author_row[2]                    
                    

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return author

    def update(self, p_author):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_author.author_id, p_author.first_name, p_author.last_name)
            cursor.callproc('updateAuthor', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)


    def delete(self, author_id):    
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args= (author_id,)
            cursor.callproc('deleteAuthor', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
    
    def getTotalAuthorRevenueByAuthorID(self, author_id):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [author_id]
            # Calls the stored procedure
            cursor.callproc('getTotalAuthorRevenueByAuthorID',args)         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    totalSum = x[0]

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return totalSum
    
    def getTotalInventoryByAuthorID(self, author_id):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [author_id]
            # Calls the stored procedure
            cursor.callproc('getTotalInventoryByAuthorID',args)         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    totalSum = x[0]

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return totalSum