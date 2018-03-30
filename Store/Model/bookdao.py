from Store.Model import book
from mysql.connector import MySQLConnection, Error
from Store.Model.dbconfig import read_db_config


def createBook(b):

    args = (b.get_isbn13(),b.get_isbn10(), b.get_title(),b.get_copyRightDate(),
            b.get_type(),b.get_edition(),b.get_numberOfPages(),b.get_size(),b.get_weight(),
            b.get_image(),b.get_genre(),b.get_authorID(),b.get_publisherID())
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        cursor.callproc('createBook',args)

        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


def getAllBooks():

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        allbooks = []
        cursor.callproc('getAllBooks')

        for result in cursor.stored_results():
            books = result.fetchall()

        for x in books:
            currentbook = book.Book()
            currentbook.set_bookID(x[0])
            currentbook.set_isbn13(x[1])
            currentbook.set_isbn10(x[2])
            currentbook.set_title(x[3])
            currentbook.set_copyRightDate(x[4])
            currentbook.set_type(x[5])
            currentbook.set_edition(x[6])
            currentbook.set_numberOfPages(x[7])
            currentbook.set_size(x[8])
            currentbook.set_weight(x[9])
            currentbook.set_image(x[10])
            currentbook.set_genre(x[11])
            currentbook.set_authorID(x[12])
            currentbook.set_publisherID(x[13])
            allbooks.append(currentbook)

        conn.commit()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return allbooks






if __name__ == '__main__':
    print(getAllBooks())

