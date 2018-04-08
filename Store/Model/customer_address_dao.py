from customer_address import CustomerAddress
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from abc_dao import AbcDao

class CustomerAddressDao(AbcDao):

    def create(self, p_customer):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_customer.street, p_customer.city, 
                    p_customer.state_code, p_customer.zip_code, p_customer.customer_id, p_customer.address_type]
            cursor.callproc('createCustomerAddress',args)

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
            args = [p_customer.address_id, p_customer.street, p_customer.city, 
                    p_customer.state_code, p_customer.zip_code, p_customer.customer_id, p_customer.address_type]
            cursor.callproc('updateCustomerAddress',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def delete(self, p_customer):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_customer.address_id, p_customer.customer_id]
            cursor.callproc('deleteCustomerAddress',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def get_all(self):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            cursor.callproc('getAllCustomerAddress')
            all_customer_address = []

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentAddress= CustomerAddress()
                currentAddress.address_id = x[0]
                currentAddress.street = x[2]
                currentAddress.city = x[3]
                currentAddress.state_code = x[4]
                currentAddress.zip_code = x[5]
                currentAddress.address_type = x[6]
                all_customer_address.append(currentAddress)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return all_customer_address
    def get_all_addresses_by_customer_id(self,p_customer):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_customer.customer_id]
            cursor.callproc('getAllCustomerAddress',args)
            all_customer_address = []

            for result in cursor.stored_results():
                customers = result.fetchall()

            for x in customers:
                currentAddress= CustomerAddress()
                currentAddress.address_id = x[0]
                currentAddress.street = x[2]
                currentAddress.city = x[3]
                currentAddress.state_code = x[4]
                currentAddress.zip_code = x[5]
                currentAddress.address_type = x[6]
                all_customer_address.append(currentAddress)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return all_customer_address