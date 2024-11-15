import sqlite3

class Inventory:
   import sqlite3

class Inventory:
    def __init__(self, database_name=""):
        self.database_name = database_name
        self.connection = None
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

   
