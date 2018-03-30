from Store.Model import publisher
from mysql.connector import MySQLConnection, Error
from Store.Model.dbconfig import read_db_config


def create_publisher(publisher_obj):
    args = (publisher_obj.companyName, publisher_obj.city, publisher_obj.stateCode, publisher_obj.zipCode)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        cursor.callproc('createPublisher', args)

        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


def get_publisher(publisher_id):
    args = (publisher_id,)
    results = None
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        cursor.callproc('getPublisher', args)
        pub = publisher.Publisher()
        results = cursor.stored_results()

    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
        return results.__next__()


if __name__ == '__main__':
    print(get_publisher(54))

    # pub = publisher.Publisher()
    # pub.companyName = "Scholastic Corporation"
    # pub.city = "New York"
    # pub.stateCode = "NY"
    # pub.zipCode = "10012"
    # create_publisher(pub)
