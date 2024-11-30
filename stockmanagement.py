import sys
import json

stock = {}

def load_stock():
    global stock
    try:
        with open("stock_data.json", "r") as file:
            stock = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, just continue with an empty stock
        pass

# Save stock data to a file
def save_stock():
    with open("stock_data.json", "w") as file:
        json.dump(stock, file, indent=4)

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

def main():
    while True:
        print("\n\t\t\t\t\t\t\t--- Stock Management System ---")
        print("\n\t\t\t\t\t\t\t\t---- WATSON ----")
        print("\t\t\t\t\t[1] Add Product \t\t\t [2] Update Product")
        print("\t\t\t\t\t[3] View all Product \t\t\t [4] Search Product")
        print("\t\t\t\t\t[5] Exit")
        choice = input("\t\t\t\t\tEnter your Choice: ").strip()

        
        
if __name__ == "__main__":
    main()
         
        