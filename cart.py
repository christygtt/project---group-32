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
        #Sets up the database connection.
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
            print(f"Error adding item(s) to cart: {e}") #catch a specific sqlite error



    def removeFromCart(self, userID, ISBN):
        #Removes from user cart
        try:
            self.cursor.execute("SELECT Quantity FROM Cart WHERE userID =? AND ISBN =?", (userID, ISBN))
            result = self.cursor.fetchone()

            if result:
                curr_quantity = result[0]
                #if the user has more than one copy
                if curr_quantity > 1:
                    new_quantity = curr_quantity - 1
                    update_query = "UPDATE Cart SET Quantity = ? WHERE userID = ? AND ISBN = ?"
                    self.cursor.execute(update_query, (new_quantity, userID, ISBN))
                    self.connection.commit()
                    self.cursor.execute("SELECT * FROM Cart WHERE userID = ? AND ISBN = ?", (userID, ISBN))
                    print(f"One copy of ISBN {ISBN} has been removed from your cart. Remaining amount: {new_quantity}")
                else:
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
            if not cart_items:
                print("**********************Your cart is empty.*************************")
                return  
            
            total_cost = 0  
            total_items = 0  
            print("****************************Order Information******************************")
            #acts similar to creating a row. assigns each item retrieved from inventory a index number
            for item in cart_items:
                price = item[1]
                quantity = item[2]
                #calculations for createOrder parameters
                total_cost += int(price) * int(quantity) 
                total_items += int(quantity)  
            print(f"Order Total: {total_cost:.2f} | {total_items}") #debug


            date = datetime.datetime.now().strftime('%Y-%m-%d') #gets current date

            print(f"Order Date: {date}") #debug

            #create order history
            order_history = OrderHistory()
            order_id = order_history.createOrder(userID, total_items, total_cost, date) #returns orderID
            print(f"Your Order ID is: {order_id}") #debug
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
           


    
