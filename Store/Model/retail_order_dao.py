from Store.Model.retail_order import RetailOrder
from Store.Model.user import User
from Store.Model.payment_info import PaymentInfo
from Store.Model.customer_address import CustomerAddress
from Store.Model.user_dao import UserDao
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.payment_info_dao import PaymentInfoDao
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error

class RetailOrderDao(AbcDao):

    def create(self, p_retail_order):
        order_id = 0
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            
            # Create an order in the retail order table of the DB
            args = (p_retail_order.customer.customer_id, 
                    p_retail_order.shipping_address.address_id,                     
                    p_retail_order.card.card_id,
                    p_retail_order.discount)
            cursor.callproc('createOrder', args)
            order_id = cursor.lastrowid
            conn.commit()

            # Get the order ID of the order just created
            result = next(cursor.stored_results())
            order_id_row = result.fetchone()
            order_id = order_id_row[0]

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)
            
        return order_id
        

    def get_byid(self,order_id):
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            order = None
            args = [order_id]
           
            cadao = CustomerAddressDao()
            pdao = PaymentInfoDao()
            # Calls the stored procedure
            cursor.callproc('getRetailOrderByOrderID', args)         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    order = RetailOrder()
                    order.order_id = x[0]
                    order.date_ordered =x[1]
                    order.discount = x[2]
                    order.total_price = x[3]
                    order.status = x[4]

                    u = User()
                    u.id = x[5]
                    u.first_name = x[6]
                    u.last_name = x[7]
                    order.customer = u

                    p = PaymentInfo()
                    p.card_id = x[8]
                    p.last_four = x[9]
                    p.card_issuer = x[10]
                    order.card = p

                    a = CustomerAddress()
                    a.address_id = x[11]
                    a.street = x[12]
                    a.city = x[13]
                    a.state_code = x[14]
                    a.zip_code = x[15]
                    order.shipping_address = a
                    
            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return order

    def get_all(self):
        orders = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            
            udao = UserDao()
            cadao = CustomerAddressDao()
            pdao = PaymentInfoDao()
            # Calls the stored procedure
            cursor.callproc('getAllRetailOrders')         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    order = RetailOrder()
                    order.order_id = x[0]
                    order.date_ordered =x[1]
                    order.total_price = x[2]
                    order.discount = x[3]
                    order.customer.id = x[4]                    
                    order.status = x[7]
                    orders.append(order)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders
    
    def getAllCancelledOrders(self):
        orders = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            
            udao = UserDao()
            cadao = CustomerAddressDao()
            pdao = PaymentInfoDao()
            # Calls the stored procedure
            cursor.callproc('getAllCancelledOrders')         
            
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    order = RetailOrder()
                    order.order_id = x[0]
                    order.date_ordered =x[1]
                    order.total_price = x[2]
                    order.discount = x[3]
                    order.customer = udao.get_byid(x[4])
                    order.shipping_address = cadao.get_byid(x[5])
                    order.card = pdao.get_byid(x[6])
                    order.status = x[7]
                    orders.append(order)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders

    def getOrdersByCustomerID(self, customer_id):
        orders = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = [customer_id]
            # Calls the stored procedure
            cursor.callproc('getRetailOrderByCustomerID', args)         
            udao = UserDao()
            cadao = CustomerAddressDao()
            pdao = PaymentInfoDao()
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    order = RetailOrder()
                    order.order_id = x[0]
                    order.date_ordered =x[1]
                    order.total_price = x[2]
                    order.discount = x[3]
                    orders.append(order)
            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders

    def update(self, order_id):
        try:
            db_config = read_db_config()        
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            
            # Create an order in the retail order table of the DB
            args = [order_id]
                    
            cursor.callproc('CancelOrder', args)
            conn.commit()

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

    def delete(self):
        raise NotImplementedError
    
    def getOrdersByCardID(self,card_id):
        orders = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = [card_id]
            # Calls the stored procedure
            cursor.callproc('getOrdersByCardID', args)         
            udao = UserDao()
            cadao = CustomerAddressDao()
            pdao = PaymentInfoDao()
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    order = RetailOrder()
                    order.order_id = x[0]
                    order.date_ordered =x[1]
                    order.total_price = x[2]
                    order.discount = x[3]
                    order.customer = udao.get_byid(x[4])
                    order.shipping_address = cadao.get_byid(x[5])
                    order.card = pdao.get_byid(x[6])
                    order.status = x[7]
                    orders.append(order)
            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders
    
    def getOrdersByShippingAddressID(self,addresss_id):
        orders = []
        try:
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = [addresss_id]
            # Calls the stored procedure
            cursor.callproc('getOrdersByShippingAddressID', args)         
            udao = UserDao()
            cadao = CustomerAddressDao()
            pdao = PaymentInfoDao()
            # This loop iterates through the resultsets
            for result in cursor.stored_results():
                # This loop iterates through the rows in each resultset
                for x in result.fetchall():
                    order = RetailOrder()
                    order.order_id = x[0]
                    order.date_ordered =x[1]
                    order.total_price = x[2]
                    order.discount = x[3]
                    order.customer = udao.get_byid(x[4])
                    order.shipping_address = cadao.get_byid(x[5])
                    order.card = pdao.get_byid(x[6])
                    order.status = x[7]
                    orders.append(order)
            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders
                                
    