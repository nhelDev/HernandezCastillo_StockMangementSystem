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

def main():
    while True:
        print("\n\t\t\t\t\t\t\t--- Stock Management System ---")
        print("\n\t\t\t\t\t\t\t\t---- WATSON ----")
        print("\t\t\t\t\t[1] Add Product \t\t\t [2] Update Product")
        print("\t\t\t\t\t[3] View all Product \t\t\t [4] Search Product")
        print("\t\t\t\t\t[5] Exit")
        choice = input("\t\t\t\t\tEnter your Choice: ").strip()
        
        if choice == "1":
            add_product()

        
        
if __name__ == "__main__":
    main()
         
        