from user import *
from cart import *
from inventory import *
from history import *
from cart import *


## COMPLETE initial pre-login menu
def initialMenu():
    ## objects for the classes
    user = User()
    cart = Cart()
    inventory = Inventory()
    history = OrderHistory()

    ## initial menu
    while(1):
        print("Pre-Login Menu:")
        print("0. Login")
        print("1. Create Account")
        print("2. Exit Program")
        initial = input("Enter your menu choice: ")
        print()

        if(initial == "0"):
            user.login()

        elif(initial == "1"):
            user.createAccount()

        ## exit program
        elif(initial == "2"):
            print("Good-bye!")
            break

        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()

        ## checks status after one menu loop...
        ## goes into main menu if applicable
        if(user.getLoggedIn()):
            mainMenu(user, cart, inventory, history)

def inventoryMenu(inventory):
    while True:
        print("Inventory Menu:")
        print("0. Go Back")
        print("1. View Inventory")
        print("2. Search Inventory")
        print("3. Decrease Stock")
        choice = input("Enter your choice: ")
        print()

        if choice == "0":
            break

        elif choice == "1":
            inventory.view_inventory()  

        elif choice == "2":
            title = input("Enter the title to search: ")
            inventory.search_inventory(title) 

        elif choice == "3":
            isbn = input("Enter the ISBN of the item: ")
            quantity = int(input("Enter the quantity to decrease: "))
            inventory.decrease_stock(isbn, quantity) 

        else:
            print("Invalid option. Please try again.")

        print()

def historyMenu(history, user):
    while True:
        print("Order History Menu")
        print("0. Go Back")
        print("1. View Order History")
        print("2. View Specific Order")
        choice = input("Enter your choice: ")
        print()

        if choice == "0":
            break 
        
        elif choice == "1":

            user_id = user.getUserID()
            orders = history.viewHistory(user_id)
            if orders:
                print("Order History:")
                for order in orders:
                    print(f"Order Number: {order[0]}, Items: {order[1]}, Cost : {order[2]}, Date: {order[3]}")
                else:
                    print("No order history found.")
                print()

        elif choice == "2":

            user_id = user.getUserID()
            order_id = input("Enter the Order Number: ")
            order_details = history.viewOrder(user_id, order_id)
            if order_details:
                print("Order Details:")
                for detail in order_details:
                    print(f"Title: {detail[1]}, Quantity: {detail[2]}, Cost: {detail[3]}")
            else:
                print("No details found for the given Order Number.")
            print()

        else:
            print("Invalid option. Please try again.")
        print()


def cartMenu(cart,User):
    while True:
        print("Cart Menu: ")
        print("0. Go Back")
        print("1. View Cart")
        print("2. Add Items To Cart")
        print("3. Remove Item From Cart")
        print("4. Checkout")

        userID = User.getUserID()
        try:
            choice = int(input("Enter your choice:"))
            print()
        except ValueError:
            print(f"Invalid choice. Please enter a valid number.")
            continue
        print()
        if choice == 0:
            break
        elif choice == 1:
            cart.viewCart(userID)
        elif choice == 2:
            ISBN = input("Enter the ISBN of the item you'd like to order: ")
            quantity = int(input("Enter the quantity of item: "))
            cart.addToCart(userID, ISBN, quantity)
        elif choice == 3:
            ISBN = input("Enter the ISBN of the item you'd like to remove: ")
            cart.removeFromCart(userID, ISBN)
        elif choice == 4:
            cart.checkOut(userID)
        else:
            print(f"Invalid. option. Please try again.")
        print()
## incomplete main menu...
def mainMenu(user, cart, inventory, history):
    while(user.getLoggedIn()):
        print("Main Menu:")
        print("0. Logout")
        print("1. View Account Information")
        print("2. Inventory Information")
        print("3. Cart Information")
        print("4. Order Information")
        option = input("Enter your menu choice: ")
        print()

        ## logging out
        if(option == "0"):
            user.logout()
            print("Logout Successful.")

        elif(option == "1"):
            user.viewAccountInformation()
            
        elif(option == "2"):
            inventoryMenu(inventory)

        elif(option == "3"):
            cartMenu(cart, user)

        elif(option == "4"):
            historyMenu(history, user)
        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()

def main():
    print("Welcome to the online bookstore!\n")

    initialMenu()

main()

