import sqlite3

class Inventory:
   import sqlite3

class Inventory:
    def __init__(self, database_name="methods.db"):
        self.database_name = database_name
        if database_name:
            self.connect_to_database()

    def connect_to_database(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.database_name)
            print("Database connected successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def view_inventory(self):
        """Displays all items in the inventory."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Inventory")
            items = cursor.fetchall()
            if items:
                print("Inventory Items:")
                for item in items:
                    print(f"ISBN: {item[0]}, Title: {item[1]}, Author: {item[2]}, "
                          f"Genre: {item[3]}, Pages: {item[4]}, Release Date: {item[5]}, "
                          f"Price: {item[6]}, Stock: {item[7]}")
            else:
                print("Inventory is empty.")
        except sqlite3.Error as e:
            print(f"Error retrieving inventory: {e}")

    def search_inventory(self, title):
        """Searches for items by title in the inventory."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Inventory WHERE Title LIKE ?", (f"%{title}%",))
            items = cursor.fetchall()
            if items:
                print("Search Results:")
                for item in items:
                    print(f"ISBN: {item[0]}, Title: {item[1]}, Author: {item[2]}, "
                          f"Genre: {item[3]}, Pages: {item[4]}, Release Date: {item[5]}, "
                          f"Price: {item[6]}, Stock: {item[7]}")
            else:
                print("No items found with that title.")
        except sqlite3.Error as e:
            print(f"Error searching inventory: {e}")

    def decrease_stock(self, ISBN, quantity=1):
        """Decreases the stock quantity of an item based on its ISBN."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT Stock FROM Inventory WHERE ISBN = ?", (ISBN,))
            result = cursor.fetchone()
            if result and result[0] >= quantity:
                new_stock = result[0] - quantity
                cursor.execute("UPDATE Inventory SET Stock = ? WHERE ISBN = ?", (new_stock, ISBN))
                self.connection.commit()
                print(f"Stock for ISBN {ISBN} decreased by {quantity}. New stock: {new_stock}.")
            elif result:
                print("Insufficient stock available.")
            else:
                print("Item not found.")
        except sqlite3.Error as e:
            print(f"Error decreasing stock: {e}")

