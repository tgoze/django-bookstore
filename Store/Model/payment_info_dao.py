from payment_info import PaymentInfo
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from abc_dao import AbcDao

class PaymentInfoDao(AbcDao):
    
    def create(self, parameter_list):
        raise NotImplementedError
    def update(self, parameter_list):
        raise NotImplementedError
    def delete(self, parameter_list):
        raise NotImplementedError
    def get_all(self, parameter_list):
        raise NotImplementedError