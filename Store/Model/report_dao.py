from Store.Model.retail_order import RetailOrder
from Store.Model.user_dao import UserDao
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.payment_info_dao import PaymentInfoDao
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao
from mysql.connector import MySQLConnection, Error
class ReportDao():

    def getJanuaryOrders(self):
            orders = []
            try:
                # Setup connection to the DB
                db_config = read_db_config()
                conn = MySQLConnection(**db_config)
                cursor = conn.cursor()

                
                # Calls the stored procedure
                cursor.callproc('getJanuaryOrders')         
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
                        orders.append(order)

                # Close the connection to the DB
                cursor.close()
                conn.close()
            except Error as error:
                print(error)
            except Exception as e:
                print(e)

            return orders
    def getJanuaryRevenue(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            cursor.callproc('getJanuaryRevenue')         
            
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
    
    def getFebruaryOrders(self):
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
                cursor.callproc('getFebruaryOrders')         
                
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
                        orders.append(order)

                # Close the connection to the DB
                cursor.close()
                conn.close()
            except Error as error:
                print(error)
            except Exception as e:
                print(e)

            return orders
    def getFebruaryRevenue(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            
            # Calls the stored procedure
            cursor.callproc('getFebruaryRevenue')         
            
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
    def getMarchOrders(self):
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
            cursor.callproc('getMarchOrders')         
            
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
                    orders.append(order)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders

    def getMarchRevenue(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            
            # Calls the stored procedure
            cursor.callproc('getMarchRevenue')         
            
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
    
    def getAprilOrders(self):
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
            cursor.callproc('getAprilOrders')         
            
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
                    orders.append(order)

            # Close the connection to the DB
            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return orders

    def getAprilRevenue(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            
            # Calls the stored procedure
            cursor.callproc('getAprilRevenue')         
            
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

    def getTotalRevenue(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            cursor.callproc('getTotalRevenue')         
            
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
    
    def getAVGTransactionAmount(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            cursor.callproc('getAVGTransactionAmount')         
            
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
    
    def getTotalNumberOfOrders(self):
        try:
            totalSum = None
            # Setup connection to the DB
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            # Calls the stored procedure
            cursor.callproc('getTotalNumberOfOrders')         
            
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