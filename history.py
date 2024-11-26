import random
import sqlite3

class OrderHistory:

    def __init__(self):
        self.databaseName = "methods.db"
        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor()
    

    def viewHistory(self, userID):
        query = "SELECT OrderNumber, ItemNumber, Cost, Date FROM Orders WHERE UserID = ?"
        self.cursor.execute(query, (userID))
        orders = self.cursor.fetchall()
        return orders

    
    def viewOrder(self, userID, orderID):
        query = """
        SELECT o.OrderNumber, i.Title, oi.Quantity, o.Cost
        FROM Orders o
        JOIN OrderItems oi ON o.OrderNumber = oi.OrderNumber
        JOIN Inventory i ON oi.ISBN = i.ISBN
        WHERE o.OrderNumber = ? AND o.UserID = ?
        """
        self.cursor.execute(query,(orderID, userID))
        order_details = self.cursor.fetchall()

        if not order_details:
            print("Error: Order does not belong to the logged-in user.")
            return None

        return order_details

    

    def createOrder(self, userID, itemNumber, cost, date):
        while True:
            orderID = str(random.randint(100000, 999999))
            self.cursor.execute("SELECT * FROM Odrers WHERE OrderNumber = ?",(orderID,))
            if not self.cursor.fetchone():
                break

        query = "INSERT INTO Orders (OrderNUmber, UserID ItemNumber, Cost Date) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (orderID, userID, itemNumber, cost, date))
        self.connection.commit() 
        return orderID


    def addOrderItems(self, userID, orderID):
        query = "SELECT ISBN, Quantity FROM Cart WHERE UserID = ?"
        self.cursor.execute(query, (userID))
        cart_items = self.cursor.fetchall()

        for isbn, quantity in cart_items:
            query = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
            self.cursor.execute(query, (orderID, isbn, quantity))
        self.connection.commit()
        query = "DELETE FROM Cart WHERE UserID = ?"
        self.cursor.execute(query, (userID,))
        self.connection.commit()    


    def closeConnection(self):
        self.cursor.close()
        self.connection.close()