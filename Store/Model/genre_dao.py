from Store.Model.genre import Genre
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error

class GenreDao(AbcDao):

    def create(self,p_genre):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_genre.genre]
            cursor.callproc('createGenre',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def delete(self, p_genre):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_genre.genre_id]
            cursor.callproc('deleteGenre', args)

            conn.commit()
        except Error as error:
            print(error)

        finally:
            cursor.close()
            conn.close()
    def update(self, p_genre):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = (p_genre.genre_id, p_genre.genre)
            cursor.callproc('updateGenre', args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def get_byid(self, genre_id):
        currentgenre = None
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [genre_id]

            cursor.callproc('getGenreByGenreID',args)


            for result in cursor.stored_results():
                genres = result.fetchall()

            for x in genres:
                currentgenre = Genre()
                currentgenre.genre_id = x[0]
                currentgenre.genre = x[1]

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return currentgenre
    def get_all(self):
        all_genres = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            cursor.callproc('getAllGenres')
            all_genres = []

            for result in cursor.stored_results():
                genres = result.fetchall()

            for x in genres:
                currentgenre = Genre()
                currentgenre.genre_id = x[0]
                currentgenre.genre = x[1]
                all_genres.append(currentgenre)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_genres
    
    def getTotalGenreRevenueByGenreID(self, genre_id):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [genre_id]
            # Calls the stored procedure
            cursor.callproc('getTotalGenreRevenueByGenreID',args)         
            
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
    
    def getTotalInventoryByGenreID(self, genre_id):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [genre_id]
            # Calls the stored procedure
            cursor.callproc('getTotalInventoryByGenreID',args)         
            
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
