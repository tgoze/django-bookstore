from inventory import Inventory
from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from abc_dao import AbcDao

class InventoryDao(AbcDao):
    def create(self, p_inventory):
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            args = [p_inventory.book_id, p_inventory.quantity_on_hand, p_inventory.quantity_ordered, p_inventory.cost, p_inventory.price]
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
            args = [p_inventory.book_id, p_inventory.quantity_on_hand, p_inventory.quantity_ordered, p_inventory.cost, p_inventory.price]
            cursor.callproc('upDateInventory',args)

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
                all_inventory.append(currentinventory)

                cursor.close()
            conn.close()
        except Error as error:
            print(error)
        except Exception as e:
            print(e)

        return all_inventory