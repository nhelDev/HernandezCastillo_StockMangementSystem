import sys
import csv

FILE_NAME = "stock_data.csv"

stock = {}

def load_stock():
    global stock
    try:
        with open(FILE_NAME, "r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stock[row["product_id"]] = {
                    "name": row["name"],
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"]),
                }
    except FileNotFoundError:
        # If the file doesn't exist, continue with an empty stock
        pass

# Save stock data to a file
def save_stock():
    with open(FILE_NAME, "w", newline='') as file:
        fieldnames = ["product_id", "name", "quantity", "price"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product_id, details in stock.items():
            writer.writerow({
                "product_id": product_id,
                "name": details["name"],
                "quantity": details["quantity"],
                "price": details["price"],
            })

# Function to add a new product
def add_product():
    product_id = input("Enter Product ID: ").strip()
    if product_id in stock:
        print("Product ID already exists. Try updating the stock instead.")
        return
    name = input("Enter Product Name: ").strip()
    try:
        quantity = int(input("Enter Initial Quantity: "))
        price = float(input("Enter Product Price: "))
    except ValueError:
        print("Invalid input. Quantity should be an integer and price should be a number.")
        return

    stock[product_id] = {"name": name, "quantity": quantity, "price": price}
    print(f"\nProduct '{name}' added successfully.")
    save_stock()  # Save the updated stock to the file

# Function to update stock quantity (restock or sell)
def update_stock():
    product_id = input("Enter Product ID: ").strip()
    if product_id not in stock:
        print("Product ID not found.")
        return

    print("\n--- Update Stock ---")
    print("1. Add stock")
    print("2. Reduce stock")
    choice = input("Enter your choice: ").strip()

    try:
        change = int(input("Enter quantity change: "))
    except ValueError:
        print("Invalid input. Quantity change should be an integer.")
        return

    if choice == "1":
        stock[product_id]["quantity"] += change
        print(f"Added {change} to '{stock[product_id]['name']}' stock. Current quantity: {stock[product_id]['quantity']}")
    elif choice == "2":
        # Ensure we are not reducing below zero stock
        if stock[product_id]["quantity"] - change < 0:
            print("Error: Insufficient stock to reduce.")
            return
        stock[product_id]["quantity"] -= change
        print(f"Reduced {change} from '{stock[product_id]['name']}' stock. Current quantity: {stock[product_id]['quantity']}")
    else:
        print("Invalid choice. Please try again.")
    save_stock()  # Save the updated stock to the file

# Function to view all stock
def view_stock():
    if not stock:
        print("\nNo products in stock.")
        return
    print("\n----------------- Current Stock -----------------")
    print(f"{'ID':<10}{'Name':<20}{'Quantity':<10}{'Price':<10}")
    for product_id, details in stock.items():
        print(f"{product_id:<10}{details['name']:<20}{details['quantity']:<10}{details['price']:<10.2f}")
    print("-------------------------------------------------")
    
    # Function to search for a product
def search_product():
    product_id = input("Enter Product ID to search: ").strip()
    if product_id not in stock:
        print("Product ID not found.")
        return
    details = stock[product_id]
    print("\n--- Product Details ---")
    print(f"Name: {details['name']}")
    print(f"Quantity: {details['quantity']}")
    print(f"Price: {details['price']:.2f}")
    print("-----------------------")

def main():
    load_stock()
    while True:
        print("\n\t\t\t\t\t\t\t--- Stock Management System ---")
        print("\n\t\t\t\t\t\t\t\t---- WATSON ----")
        print("\t\t\t\t\t[1] Add Product \t\t\t [2] Update Product")
        print("\t\t\t\t\t[3] View all Product \t\t\t [4] Search Product")
        print("\t\t\t\t\t[5] Exit")
        choice = input("\t\t\t\t\tEnter your Choice: ").strip()
        
        if choice == "1":
            add_product()
        elif choice == "2":
            update_stock()
        elif choice == "3":
            view_stock()
        elif choice == "4":
            search_product()
        elif choice == "5":
            print("Exiting Stock Management System. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

        
        
if __name__ == "__main__":
    main()
         
        