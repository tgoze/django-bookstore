from Store.Model.book import Book
from Store.Model.publisher import Publisher
from Store.Model.author import Author
from Store.Model.genre import Genre
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error

class BookDao(AbcDao):

    def create(self, b):

        args = (b.get_isbn13(),b.get_isbn10(), b.get_title(),b.get_copyRightDate(),
                b.get_type(),b.get_edition(),b.get_numberOfPages(),
                b.get_genre().genre_id,b.get_author().author_id,b.get_publisher().publisher_id,
                b.inventory.quantity_on_hand, b.inventory.cost, b.inventory.retail_price)
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


    def update(self, b):
        args = (b.get_book_id(), b.get_isbn13(), b.get_isbn10(), b.get_title(), b.get_copyRightDate(),
                b.get_type(), b.get_edition(), b.get_numberOfPages(), 
                b.get_genre().genre_id, b.get_author().author_id, b.get_publisher().publisher_id)
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            cursor.callproc('updateBook', args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()


    def get_byid(self, book_id):    
        book = Book()
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (book_id,)
            cursor.callproc('getBookByID', args)                
            # This gets the first resultset
            result = next(cursor.stored_results())
            # This gets the first row in the resultset
            book_row = result.fetchone()
            book.set_book_id(book_row[0])
            book.set_isbn13(book_row[1])
            book.set_isbn10(book_row[2])
            book.set_title(book_row[3])
            book.set_copyRightDate(book_row[4])
            book.set_type(book_row[5])
            book.set_edition(book_row[6])
            book.set_numberOfPages(book_row[7])

            genre = Genre()
            genre.genre_id = book_row[8]
            genre.genre = book_row[14]
            author = Author()
            author.author_id = book_row[9]
            author.first_name = book_row[12]
            author.last_name = book_row[13]
            publisher = Publisher()
            publisher.publisher_id = book_row[10]
            publisher.company_name = book_row[11]
            book.set_genre(genre)
            book.set_author(author)
            book.set_publisher(publisher)

            book.inventory.quantity_on_hand = book_row[15]
            book.inventory.quantity_ordered = book_row[16]
            book.inventory.cost = book_row[17]
            book.inventory.retail_price = book_row[18]

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return book


    def get_all(self):
        allBooks = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            cursor.callproc('getAllBooks')            

            for result in cursor.stored_results():
                books = result.fetchall()

            for x in books:

                currentbook = Book()
                currentbook.set_book_id(x[0])
                currentbook.set_isbn13(x[1])
                currentbook.set_isbn10(x[2])
                currentbook.set_title(x[3])
                currentbook.set_copyRightDate(x[4])
                currentbook.set_type(x[5])
                currentbook.set_edition(x[6])
                currentbook.set_numberOfPages(x[7])

                genre = Genre()
                genre.genre_id = x[8]
                genre.genre = x[14]
                author = Author()
                author.author_id = x[9]
                author.first_name = x[12]
                author.last_name = x[13]
                publisher = Publisher()
                publisher.publisher_id = x[10]
                publisher.company_name = x[11]
                currentbook.set_genre(genre)
                currentbook.set_author(author)
                currentbook.set_publisher(publisher)

                currentbook.inventory.quantity_on_hand = x[15]
                currentbook.inventory.quantity_ordered = x[16]
                currentbook.inventory.cost = x[17]
                currentbook.inventory.retail_price = x[18]

                allBooks.append(currentbook)

            conn.commit()
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
            
        return allBooks

    
    def getBooksByGenreID(self, genre_id):
        allBooks = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [genre_id]
            cursor.callproc('getBooksByGenreID', args)
         

            for result in cursor.stored_results():
                books = result.fetchall()

            for x in books:

                currentbook = Book()
                currentbook.set_book_id(x[0])
                currentbook.set_isbn13(x[1])
                currentbook.set_isbn10(x[2])
                currentbook.set_title(x[3])
                currentbook.set_copyRightDate(x[4])
                currentbook.set_type(x[5])
                currentbook.set_edition(x[6])
                currentbook.set_numberOfPages(x[7])
                currentbook.set_genre(x[8])
                currentbook.set_author(x[9])
                currentbook.set_publisher(x[10])
                allBooks.append(currentbook)

            conn.commit()
        except Error as error:
            print(error)

        finally:
            cursor.close()
            conn.close()
        return allBooks

    def getBooksByPublisherID(self, publisher_id):
        allBooks = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [publisher_id]
            cursor.callproc('getBooksByPublisherID', args)
         

            for result in cursor.stored_results():
                books = result.fetchall()

            for x in books:

                currentbook = Book()
                currentbook.set_book_id(x[0])
                currentbook.set_isbn13(x[1])
                currentbook.set_isbn10(x[2])
                currentbook.set_title(x[3])
                currentbook.set_copyRightDate(x[4])
                currentbook.set_type(x[5])
                currentbook.set_edition(x[6])
                currentbook.set_numberOfPages(x[7])
                currentbook.set_genre(x[8])
                currentbook.set_author(x[9])
                currentbook.set_publisher(x[10])
                allBooks.append(currentbook)

            conn.commit()
        except Error as error:
            print(error)

        finally:
            cursor.close()
            conn.close()
        return allBooks
    # def getBooksByAuthor(self, b,c):
    #     try:
    #         db_config = read_db_config()
    #         conn = MySQLConnection(**db_config)
    #         cursor = conn.cursor()
    #         args = [b,c]
    #         cursor.callproc('getBooksByAuthor', args)
    #         allBooks = []

    #         for result in cursor.stored_results():
    #             books = result.fetchall()

    #         for x in books:

    #             currentbook = Book()
    #             currentbook.set_bookID(x[3])
    #             currentbook.set_isbn13(x[4])
    #             currentbook.set_isbn10(x[5])
    #             currentbook.set_title(x[6])
    #             currentbook.set_copyRightDate(x[7])
    #             currentbook.set_type(x[8])
    #             currentbook.set_edition(x[9])
    #             currentbook.set_numberOfPages(x[10])
    #             currentbook.set_image(x[11])
    #             currentbook.set_genre(x[12])
    #             currentbook.set_authorID(x[13])
    #             currentbook.set_publisherID(x[14])
    #             allBooks.append(currentbook)



    #         conn.commit()
    #     except Error as error:
    #         print(error)

    #     finally:
    #         cursor.close()
    #         conn.close()
    #     return allBooks


    # def getBookbyTitle(self, title):
    #     try:
    #         db_config = read_db_config()
    #         conn = MySQLConnection(**db_config)
    #         cursor = conn.cursor()

    #         args = [title]

    #         cursor.callproc('getBookByTitle', args)

    #         for result in cursor.stored_results():
    #             books = result.fetchall()

    #         for x in cursor.stored_results():
    #             currentbook = Book()
    #             currentbook.set_bookID(x[0])
    #             currentbook.set_isbn13(x[1])
    #             currentbook.set_isbn10(x[2])
    #             currentbook.set_title(x[3])
    #             currentbook.set_copyRightDate(x[4])
    #             currentbook.set_type(x[5])
    #             currentbook.set_edition(x[6])
    #             currentbook.set_numberOfPages(x[7])
    #             currentbook.set_image(x[8])
    #             currentbook.set_genre(x[9])
    #             currentbook.set_authorID(x[10])
    #             currentbook.set_publisherID(x[11])



    #         conn.commit()
    #     except Error as error:
    #         print(error)

    #     finally:
    #         cursor.close()
    #         conn.close()
    #     return currentbook


    # def searchBooks(python, b):
    #     try:
    #         db_config = read_db_config()
    #         conn = MySQLConnection(**db_config)
    #         cursor = conn.cursor()
    #         args = [b]
    #         cursor.callproc('searchBooks', args)
    #         allBooks = []

    #         for result in cursor.stored_results():
    #             books = result.fetchall()

    #         for x in books:

    #             currentbook = Book()
    #             currentbook.set_bookID(x[0])
    #             currentbook.set_isbn13(x[1])
    #             currentbook.set_isbn10(x[2])
    #             currentbook.set_title(x[3])
    #             currentbook.set_copyRightDate(x[4])
    #             currentbook.set_type(x[5])
    #             currentbook.set_edition(x[6])
    #             currentbook.set_numberOfPages(x[7])
    #             currentbook.set_image(x[8])
    #             currentbook.set_genre(x[9])
    #             currentbook.set_authorID(x[10])
    #             currentbook.set_publisherID(x[11])
    #             allBooks.append(currentbook)



    #         conn.commit()
    #     except Error as error:
    #         print(error)

    #     finally:
    #         cursor.close()
    #         conn.close()
    #     return allBooks


    def delete(self, b):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [b]
            cursor.callproc('deleteBook', args)

            conn.commit()
        except Error as error:
            print(error)

        finally:
            cursor.close()
            conn.close()
