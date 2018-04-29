from Store.Model.customer_info import CustomerInfo
from Store.Model.user_dao import UserDao
from Store.Model.user import User
from Store.Model.customer_address import CustomerAddress
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error
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
            args = [p_customer.customer_id, p_customer.work_phone, p_customer.home_phone, 
                p_customer.user.first_name, p_customer.user.last_name, p_customer.user.email]
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

            cursor.callproc('getAllCustomerUserInfo')
            all_customer_info = []

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo = CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.work_phone = x[1]
                currentinfo.home_phone = x[2]
                u = User()
                u.id = x[3]
                u.password = x[4]
                u.last_login = x[5]
                u.is_superuser = x[6]
                u.username = x[7]
                u.first_name = x[8]
                u.last_name = x[9]
                u.email = x[10]
                u.is_staff = x[11]
                u.is_active = x[12]
                u.date_joined = x[13]
                currentinfo.set_user(u)
                all_customer_info.append(currentinfo)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return all_customer_info
    def get_all_CAddress(self):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            cursor.callproc('getAllCustomerInfo')
            all_customer_info = []

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo = CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.work_phone = x[1]
                currentinfo.home_phone = x[2]
                a = CustomerAddress()
                a.address_id = x[3]
                a.street = x[4]
                a.city = x[5]
                a.state_code = x[6]
                a.address_type = x[8]
                currentinfo.set_address(a)
                all_customer_info.append(currentinfo)
                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_customer_info
    def get_byid(self, id):
        currentinfo = None
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [id]
            cursor.callproc('getCustomerUserInfoById',args)
            

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo= CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.work_phone = x[1]
                currentinfo.home_phone = x[2]
                u = User()
                u.id = x[3]
                u.password = x[4]
                u.last_login = x[5]
                u.is_superuser = x[6]
                u.username = x[7]
                u.first_name = x[8]
                u.last_name = x[9]
                u.email = x[10]
                u.is_staff = x[11]
                u.is_active = x[12]
                u.date_joined = x[13]
                currentinfo.set_user(u)
                
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return currentinfo
    def get_addressbyid(self, id):
        currentinfo = None
        all_customer = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [id]
            cursor.callproc('getCustomerAddressById',args)
            

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo = CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.work_phone = x[1]
                currentinfo.home_phone = x[2]
                a = CustomerAddress()
                a.address_id = x[3]
                a.street = x[4]
                a.city = x[5]
                a.state_code = x[6]
                a.address_type = x[9]
                currentinfo.set_address(a)
                all_customer.append(currentinfo)
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_customer
    
    def getRepeatCustomers(self):
        currentinfos = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            
            cursor.callproc('getRepeatCustomers')
            print('hit')

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentinfo = CustomerInfo()
                currentinfo.customer_id = x[0]
                currentinfo.number_of_orders = x[1]
                currentinfos.append(currentinfo)
                
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return currentinfos