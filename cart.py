class Cart:

    def __init__(self):
        sample = ""
    def __init__(self,database_name = "methods.db"):
        self.connection = sqlite3.connect("methods.db")
        self.cursor = self.connection.cursor()
        
    def viewCart(self, userID):
        
        try:
            query = """
                SELECT Inventory.Title, Inventory.ISBN, Inventory.Price, Cart.Quantity
                FROM Cart
                INNER JOIN Inventory ON Cart.ISBN = Inventory.ISBN
                WHERE Cart.UserID = ?;
        """
            cursor.execute(query, (userID,))
            result = cursor.fetchall()
        
            if not result:
                print("User Cart is empty.")
            else:
                print("User Cart: ")
                cart_Cost = 0.0
                for row in result:
                    row = Inventory.title, Inventory.ISBN, Inventory.Price, Cart.quantity
                    
                    item_cost = float(price) * int(quantity)
                    cart_cost += item_cost
                    print(f"Title: {title}")
                    print(f"ISBN: {isbn}")
                    print(f"Price: {price:.2f} | Quantity: {quantity} | Item Total: {item_cost:.2f}")
                print(f"Total Cart Cost: ${cart_cost:.2f}")  
        except:
            print(f"An error occured. Please try again.")
    def addToCart(self,userID, ISBN, quantity = 1):
        query = "INSERT INTO Cart (userID,ISBN, quantity) VALUES (?, ?, ?)"
        data = (userID, ISBN, quantity)

        try:
            ## sends query and data
            cursor.execute(query, data)

            ## commits change
            self.connection.commit()

            ## shows changes
            print(cursor.rowcount, "book(s) added to cart.")
            print()
        except:
            print("Error adding item(s) to cart.")
        
    def removeFromCart(self,userID,ISBN):
        try:
            query = "DELETE FROM Cart WHERE userID = ? AND ISBN=?"

            ## deleting --> weird quirk where you need to have a second blank item
            ## so the tuple has ", " at the end of it, no matter how many items used
            data = (userID,IBSN,)

            ## sends query and data
            self.cursor.execute(query, data)

            ## commits change
            self.connection.commit()

            ## shows changes
            print(self.cursor.rowcount, "item(s) deleted.")
            print()
        except:
            print("Error removing item(s) from cart.")

                    

        
        