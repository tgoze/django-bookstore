from publisher import Publisher
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from abc_dao import AbcDao

class PublisherDao(AbcDao):

    def create(self, p_publisher):    
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_publisher.company_name, p_publisher.city, p_publisher.state_code, p_publisher.zip_code)
            cursor.callproc('createPublisher', args)
            conn.commit()

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)


    def get_all(self):    
        publishers = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            cursor.callproc('getAllPublishers')         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for publisher_row in result.fetchall():
                    publisher = Publisher()
                    publisher.publisher_id = publisher_row[0]
                    publisher.company_name = publisher_row[1]
                    publisher.city = publisher_row[2]
                    publisher.state_code = publisher_row[3]
                    publisher.zip_code = publisher_row[4]
                    publishers.append(publisher)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return publishers

    def get_byname(self, company_name):    
        publisher = Publisher()
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (company_name,)
            cursor.callproc('getPublisherByName', args)                
            # This gets the first resultset
            result = next(cursor.stored_results())
            # This gets the first row in the resultset
            publisher_row = result.fetchone()
            publisher.publisher_id = publisher_row[0]
            publisher.company_name = publisher_row[1]
            publisher.city = publisher_row[2]
            publisher.state_code = publisher_row[3]
            publisher.zip_code = publisher_row[4]
            leftover_rows = len(result.fetchall())
            # Probably don't need this since we should make the company name a UI
            if leftover_rows != 0:
                print(str(leftover_rows) + " more row(s) have the company name: " + "\"" + company_name + "\"")   

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return publisher


    def update(self, p_publisher):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_publisher.publisher_id, p_publisher.company_name, p_publisher.city, p_publisher.state_code, p_publisher.zip_code)
            cursor.callproc('updatePublisher', args)
            conn.commit()

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)


    def delete(self, publisher_id):    
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args= (publisher_id,)
            cursor.callproc('deletePublisher', args)
            conn.commit()
            print(str(cursor.rowcount) + " row(s) were affected.")

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
