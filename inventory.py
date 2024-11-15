import sqlite3

class Inventory:
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName
        try:
         self.connection = sqlite3.connect(self.databaseName)
         print("Database connected successfully.")
        except Exception as e:
         print("Failed to connect to database:", e)

    def view_inventory(self):
        """Displays all items in the inventory."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Inventory")
            items = cursor.fetchall()
            if items:
                print("Inventory Items:")
                for item in items:
                    print(item)
            else:
                print("Inventory is empty.")
        except sqlite3.Error as e:
            print(f"Error retrieving inventory: {e}")

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

   
