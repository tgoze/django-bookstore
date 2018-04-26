from Store.Model.payment_info import PaymentInfo
from Store.Model.customer_address import CustomerAddress
from mysql.connector import MySQLConnection, Error
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao

class PaymentInfoDao(AbcDao):
    
    def create(self, p_payment):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_payment.card_number, p_payment.cvc, p_payment.expir_date, p_payment.card_issuer,
                    p_payment.customer_id, p_payment.billing_address.address_id]
            cursor.callproc('createPaymentInfo',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

    def update(self, p_payment):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_payment.card_id, p_payment.card_number, p_payment.cvc, p_payment.expir_date, 
                    p_payment.card_issuer, p_payment.customer_id, p_payment.billing_address.address_id]
            cursor.callproc('updatePaymentInfo',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

    def delete(self, p_payment):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_payment.card_id]
            cursor.callproc('deletePaymentInfo', args)

            conn.commit()
        except Error as error:
            print(error)

        finally:
            cursor.close()
            conn.close()
        
    def get_by_address_id(self,p_address_id, p_customer_id,):
        all_payments = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_address_id, p_customer_id]
            cursor.callproc('getPaymentInfoByAddressID',args)
            

            for result in cursor.stored_results():
                payments = result.fetchall()

            for x in payments:
                currentpayment = PaymentInfo()
                currentpayment.card_id = x[0]
                currentpayment.last_four = x[2]
                currentpayment.expir_date = x[3]    
                currentpayment.card_issuer = x[4]            
                currentpayment.customer_id = x[5]
                currentpayment.billing_address_id = x[6]
                all_payments.append(currentpayment)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return all_payments
    
    def get_by_customer_id(self, customer_id):
        all_payments = []
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [customer_id]
            cursor.callproc('getAllPaymentInfoByCustomerID', args)
            

            for result in cursor.stored_results():
                payments = result.fetchall()

            for x in payments:
                currentpayment = PaymentInfo()
                currentpayment.card_id = x[0]
                currentpayment.last_four = x[1]
                currentpayment.expir_date = x[2]    
                currentpayment.card_issuer = x[3]            
                currentpayment.customer_id = x[4]
                currentpayment.billing_address.address_id = x[5]
                currentpayment.billing_address.street = x[6]
                currentpayment.billing_address.city = x[7]
                currentpayment.billing_address.state_code = x[8]
                currentpayment.billing_address.zip_code = x[9]
                currentpayment.billing_address.address_type = x[10]

                all_payments.append(currentpayment)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return all_payments

    def get_byid(self,card_id):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [card_id]
            cursor.callproc('getPaymentInfoByCardID', args)
            

            for result in cursor.stored_results():
                payments = result.fetchall()

            for x in payments:
                currentpayment = PaymentInfo()
                currentpayment.card_id = x[0]
                currentpayment.last_four = x[1]
                currentpayment.expir_date = x[2]    
                currentpayment.card_issuer = x[3]            
                currentpayment.customer_id = x[4]
                currentpayment.billing_address.address_id = x[5]
                currentpayment.billing_address.street = x[6]
                currentpayment.billing_address.city = x[7]
                currentpayment.billing_address.state_code = x[8]
                currentpayment.billing_address.zip_code = x[9]
                currentpayment.billing_address.address_type = x[10]
                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
        return currentpayment
    
    def get_all(self): 
        raise NotImplementedError