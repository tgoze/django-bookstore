from Store.Model.inventory import Inventory
from Store.Model.book_dao import BookDao
from mysql.connector import MySQLConnection, Error
from Store.Model.dbconfig import read_db_config
from Store.Model.abc_dao import AbcDao

class InventoryDao(AbcDao):
    def create(self, p_inventory):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_inventory.book_id, p_inventory.quantity_on_hand, p_inventory.quantity_ordered, p_inventory.cost, p_inventory.retail_price]
            cursor.callproc('createInventory',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def update(self, p_inventory):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_inventory.book_id, p_inventory.quantity_on_hand, p_inventory.quantity_ordered, p_inventory.cost, p_inventory.retail_price]
            cursor.callproc('updateInventory',args)

            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
    def delete(self, p_inventory):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_inventory.book_id]
            cursor.callproc('deleteInventory', args)

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

            cursor.callproc('getAllInventory')
            all_inventory = []

            for result in cursor.stored_results():
                inventories = result.fetchall()

            for x in inventories:
                currentinventory = Inventory()
                currentinventory.book_id = x[0]
                currentinventory.quantity_on_hand = x[1]
                currentinventory.quantity_ordered = x[2]
                currentinventory.cost = x[3]
                currentinventory.retail_price = x[4]
                bdao = BookDao()
                currentinventory.book = bdao.get_byid(currentinventory.book_id)
                all_inventory.append(currentinventory)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_inventory

    def get_byid(self, book_id):
        inventory = Inventory()
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = (book_id,)
            cursor.callproc('getInventoryByID', args)                
            # This gets the first resultset
            result = next(cursor.stored_results())
            # This gets the first row in the resultset
            inventory_row = result.fetchone()
            inventory.book_id = inventory_row[0]
            inventory.quantity_on_hand = inventory_row[1]
            inventory.quantity_ordered = inventory_row[2]
            inventory.cost = inventory_row[3]
            inventory.retail_price = inventory_row[4]
            

            cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return inventory
    
    def getInventoryByGenre(self,genre_id):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = [genre_id]

            cursor.callproc('getInventoryByGenre',args)
            all_inventory = []
            bdao = BookDao()
            for result in cursor.stored_results():
                inventories = result.fetchall()

            for x in inventories:
                currentinventory = Inventory()

                currentinventory.book_id = bdao.get_byid(x[0])
                currentinventory.quantity_on_hand = x[1]
                currentinventory.quantity_ordered = x[2]
                all_inventory.append(currentinventory)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_inventory
    
    def getInventoryByPublisher(self,publisher_id):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = [publisher_id]

            cursor.callproc('getInventoryByPublisher',args)
            all_inventory = []
            bdao = BookDao()
            for result in cursor.stored_results():
                inventories = result.fetchall()

            for x in inventories:
                currentinventory = Inventory()

                currentinventory.book_id = bdao.get_byid(x[0])
                currentinventory.quantity_on_hand = x[1]
                currentinventory.quantity_ordered = x[2]
                all_inventory.append(currentinventory)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_inventory
    
    def getInventoryByAuthor(self,author_id):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()

            args = [author_id]

            cursor.callproc('getInventoryByAuthor',args)
            all_inventory = []
            bdao = BookDao()
            for result in cursor.stored_results():
                inventories = result.fetchall()

            for x in inventories:
                currentinventory = Inventory()

                currentinventory.book_id = bdao.get_byid(x[0])
                currentinventory.quantity_on_hand = x[1]
                currentinventory.quantity_ordered = x[2]
                all_inventory.append(currentinventory)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_inventory