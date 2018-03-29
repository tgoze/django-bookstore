from Store.Model import book
from mysql.connector import MySQLConnection, Error
from Store.Model.dbconfig import read_db_config


def createBook(b):

    args = (b.get_bookID(),b.get_isbn13(),b.get_isbn10(), b.get_title(),b.get_copyRightDate(),
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

if __name__ == '__main__':
    x = book.Book()
    x.set_bookID(469247)
    x.set_isbn13(9999999999999)
    x.set_isbn10(3333333333)
    x.set_title('Harry Potter')
    x.set_copyRightDate('2018-03-28')
    x.set_type('paperback')
    x.set_edition(9)
    x.set_numberOfPages(500)
    x.set_size(5)
    x.set_weight(8)
    x.set_image('image5')
    x.set_genre(31)
    x.set_authorID(11)
    x.set_publisherID(53)
    createBook(x)