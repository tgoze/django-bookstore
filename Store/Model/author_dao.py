from author import Author
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from abc_dao import AbcDao

class AuthorDao(AbcDao):

    def create(self, p_author):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (p_author.first_name, p_author.last_name)
            cursor.callproc('createAuthor', args)
            conn.commit()

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        
    def get_all(self, parameter_list):
        raise NotImplementedError

    def update(self, parameter_list):
        raise NotImplementedError

    def delete(self, parameter_list):
        raise NotImplementedError

if __name__ == '__main__':

    aut = Author()
    aut.first_name = "Clide"
    aut.last_name = "Staples"

    aut_dao = AuthorDao()
    aut_dao.create(aut)
