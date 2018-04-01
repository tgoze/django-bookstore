from publisher import Publisher
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config


def create_publisher(publisher_obj):
    args = (publisher_obj.company_name, publisher_obj.city, publisher_obj.state_code, publisher_obj.zip_code)
    try:
        db_config = read_db_config()        
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

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
    args = (company_name,)
    publisher = Publisher()
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

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
        if leftover_rows != 0:
            print(str(leftover_rows) + " more row(s) have the company name: " + "\"" + company_name + "\"")   

        cursor.close()
        conn.close()
    except Error as error:
        print(error)
    except Exception as e:
        print(e)

    return publisher

if __name__ == '__main__':
    print(get_publisher_byname('test').zip_code)

    # pub = Publisher()
    # pub.companyName = "test"
    # pub.city = "test"
    # pub.stateCode = "te"
    # pub.zipCode = "teste"
    # create_publisher(pub)
