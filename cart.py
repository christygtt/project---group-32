from inventory import Inventory 
from history import OrderHistory
import sqlite3
import datetime

class Cart:

    def __init__(self, database_name = "methods.db"):
        #Zero constructor to allow the class to initialize without parameters.
        self.database_name = database_name
        self.connection = None
        self.cursor = None
        self.cartDB()

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
                print(f"***********************************Cart***************************************")
                for row in result:
                    title, ISBN, price, quantity = row

                    item_cost = float(price) * int(quantity)
                    cart_Cost += item_cost

                    print(f"Title: {title}")
                    print(f"ISBN: {ISBN}")
                    print(f"Price: {price:.2f} | Quantity: {quantity} | Item Total: {item_cost:.2f}")
                    print(f"******************************************************************************")

                print(f"******************************************************************************")
                print(f"Total Cart Cost: ${cart_Cost:.2f}")  

        except :
            print("An error occurred while viewing the cart.")

    def addToCart(self, userID, ISBN, quantity=1):
        try:
            self.cursor.execute("SELECT * FROM Inventory WHERE ISBN = ?", (ISBN,))
            item = self.cursor.fetchone()

            if not item:
                print("ISBN {ISBN} does not exist in the inventory.")
                return
            query = "INSERT INTO Cart (userID, ISBN, quantity) VALUES (?, ?, ?)"
            data = (userID, ISBN, quantity)
            self.cursor.execute(query, data)
            print(f"Added {quantity} copy(s) of {ISBN} to the cart.")
            
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding item(s) to cart: {e}")



    def removeFromCart(self, userID, ISBN):
        #Removes from user cart
        try:
            self.cursor.execute("SELECT * FROM Cart WHERE userID = ? AND ISBN = ?", (userID, ISBN))
            if self.cursor.fetchone():
                query = "DELETE FROM Cart WHERE userID = ? AND ISBN = ?"
                data = (userID, ISBN)

                self.cursor.execute(query, data)
                self.connection.commit()

                print(f"All copies of ISBN {ISBN} has been deleted from cart.")
            else:
                print("Item not found in cart.")
        except sqlite3.Error as e:
            print(f"Error removing item(s) to cart: {e}")


    def checkOut(self, userID):
        try:
            query = """
                SELECT Inventory.ISBN, Inventory.Price, Cart.Quantity
                FROM Cart
                INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN
                WHERE Cart.userID = ?;
            """
            self.cursor.execute(query, (userID,))

            cart_items = self.cursor.fetchall()
            
            print(f"*********************************************************")
            print(f"                Current items in cart                    ")
            print(f"**************************Cart***************************")
            print(f"                      {cart_items}")
            if not cart_items:
                print("               Your cart is empty.                       ")
                return
            
            total_cost = 0  
            total_items = 0  


            for item in cart_items:
                price = item[1]
                quantity = item[2]
                
                total_cost += price * quantity  
                total_items += quantity  
            print(f"{total_cost} | {total_items}")


            date = datetime.datetime.now().strftime('%Y-%m-%d')

            print(f"The Current Date is: {date}")

            order_history = OrderHistory()
            order_id = order_history.createOrder(userID, total_items, total_cost, date)
            print(f"Your Order ID is: {order_id}")
            order_history.addOrderItems(userID, order_id)

            inventory = Inventory(self.database_name)  
            for item in cart_items:
                isbn = item[0]
                quantity = item[2]
                inventory.decrease_stock(isbn, quantity)


            print("********************Checkout complete!*******************")  

        except sqlite3.Error as e:
            print(f"Error checking : {e}")

    def closeConnection(self):
        self.cursor.close()
        self.connection.close()  
           


    
