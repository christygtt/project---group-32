from inventory import Inventory 
from history import OrderHistory
import sqlite3

class Cart:

    def __init__(self):
        #Zero constructor to allow the class to initialize without parameters.
        pass

    def cartDB(self, database_name="methods.db"):
        """Sets up the database connection."""
        self.database_name = database_name
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def viewCart(self, userID):
        #Displays all books in the user's cart.
        try:
            query = """
                SELECT Inventory.Title, Inventory.ISBN, Inventory.Price, Cart.Quantity
                FROM Cart
                INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN
                WHERE Cart.UserID = ?;
            """
            self.cursor.execute(query, (userID,))
            result = self.cursor.fetchall()

            if not result:
                print("User Cart is empty.")
            else:
                print("User Cart: ")
                cart_Cost = 0.0
                for row in result:
                    title, ISBN, price, quantity = row

                    item_cost = float(price) * int(quantity)
                    cart_Cost += item_cost

                    print(f"***********************************Cart***************************************")
                    print(f"Title: {title}")
                    print(f"ISBN: {ISBN}")
                    print(f"Price: {price:.2f} | Quantity: {quantity} | Item Total: {item_cost:.2f}")
                    print(f"******************************************************************************")
                print(f"Total Cart Cost: ${cart_Cost:.2f}")  

        except :
            print("An error occurred while viewing the cart.")

    def addToCart(self, userID, ISBN, quantity=1):
        #Adds to user cart
        try:
            query = "INSERT INTO Cart (userID, ISBN, quantity) VALUES (?, ?, ?)"
            data = (userID, ISBN, quantity)
            self.cursor.execute(query, data)
            self.connection.commit()
            print(f"{self.cursor.rowcount} book(s) added to cart.")
        except:
            print("Error adding item(s) to cart.")

    def removeFromCart(self, userID, ISBN):
        #Removes from user cart
        try:
            query = "DELETE FROM Cart WHERE userID = ? AND ISBN = ?"
            data = (userID, ISBN)

            self.cursor.execute(query, data)
            self.connection.commit()

            print(f"{self.cursor.rowcount} item(s) deleted from cart.")
        except:
            print("Error removing item(s) from cart.")

    def checkOut(self, userID):
        try:
            query = """
                    SELECT Inventory.ISBN, Inventory.Price, Cart.Quantity
                    FROM Cart
                    INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN
                    WHERE Cart.UserID = ?;
                """
            self.cursor.execute(query, (userID,))
            cart_items = self.cursor.fetchall()
            
            if not cart_items:
                print("Cart is empty.")
                return
            else:
                # initiates classes with database as parameter
                inventory = Inventory(self.database_name)
                order_history = OrderHistory(self.database_name)
                order_id = order_history.createOrder(userID)

                for row in cart_items:
                    isbn, price, quantity = row
                    inventory.decrease_stock(isbn,quantity)
                    order_history.addOrderItems(order_id, isbn, quantity, price)
                
                # delete all items from cart after checking out
                query = "DELETE FROM Cart WHERE UserID = ?"
                data = (userID)

                self.cursor.execute(query, data)
                self.connection.commit()
                print("Checkout complete.")
        except:
            print("Error completing Checkout. Please try again.")


        
