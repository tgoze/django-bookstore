from publisher import Publisher
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config


def create_publisher(p_publisher):    
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


def getall_publishers():    
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
            for publisherRow in result.fetchall():
                publisher = Publisher()
                publisher.publisher_id = publisherRow[0]
                publisher.company_name = publisherRow[1]
                publisher.city = publisherRow[2]
                publisher.state_code = publisherRow[3]
                publisher.zip_code = publisherRow[4]
                publishers.append(publisher)

        # Close the connection to the DB
        cursor.close()
        conn.close()
    except Error as error:
        print(error)
    except Exception as e:
        print(e)

    return publishers

def get_publisher_byname(company_name):    
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
        publisherRow = result.fetchone()
        publisher.publisher_id = publisherRow[0]
        publisher.company_name = publisherRow[1]
        publisher.city = publisherRow[2]
        publisher.state_code = publisherRow[3]
        publisher.zip_code = publisherRow[4]
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


def update_publisher(p_publisher):
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


def delete_publisher(publisher_id):    
    try:
        db_config = read_db_config()        
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        args= (publisher_id,)
        cursor.callproc('deletePublisher', args)
        conn.commit()

        cursor.close()
        conn.close()
    except Error as error:
        print(error)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    delete_publisher(55)
    # pub = Publisher()
    # pub.publisher_id = 55
    # pub.company_name = "test"
    # pub.city = "test"
    # pub.state_code = "te"
    # pub.zip_code = "teste"
    # update_publisher(pub)
