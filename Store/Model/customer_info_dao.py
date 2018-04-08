from customer_info import CustomerInfo
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from abc_dao import AbcDao

class CustomerInfoDAO(AbcDao):
    def create(self, p_customer):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_customer.customer_id, p_customer.work_phone, p_customer.home_phone]
            cursor.callproc('createCustomerInfo',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def update(self, p_customer):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_customer.customer_id, p_customer.work_phone, p_customer.home_phone]
            cursor.callproc('updateCustomerInfo',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def delete(self, p_customer):
        raise NotImplementedError
    def get_all(self):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            cursor.callproc('getAllCustomerInfo')
            all_customer_info = []

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo= CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.work_phone = x[1]
                currentinfo.home_phone = x[2]
                all_customer_info.append(currentinfo)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_customer_info
    def get_by_id(self, id):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [id]
            cursor.callproc('getCustomerInfoByID',args)
            

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo= CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.work_phone = x[1]
                currentinfo.home_phone = x[2]

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return currentinfo