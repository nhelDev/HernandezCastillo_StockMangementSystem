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
                    "category": row.get("category", "Unknown"),  # Default to 'Unknown' if missing
                }
    except FileNotFoundError:
        # If the file doesn't exist, continue with an empty stock
        pass


# Save stock data to a file
def save_stock():
    with open(FILE_NAME, "w", newline='') as file:
        fieldnames = ["product_id", "name", "quantity", "price", "category"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product_id, details in stock.items():
            writer.writerow({
                "product_id": product_id,
                "name": details["name"],
                "quantity": details["quantity"],
                "price": details["price"],
                "category": details["category"],
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

    print("\nSelect Category:")
    print("1. Cleanser")
    print("2. Moisturizer")
    print("3. Serum")
    print("4. Sunscreen")
    category_choice = input("Enter your choice: ").strip()

    categories = {
        "1": "Cleanser",
        "2": "Moisturizer",
        "3": "Serum",
        "4": "Sunscreen"
    }
    category = categories.get(category_choice, None)
    if not category:
        print("Invalid category choice. Product not added.")
        return

    stock[product_id] = {"name": name, "quantity": quantity, "price": price, "category": category}
    print(f"\nProduct '{name}' added successfully under category '{category}'.")
    save_stock()  # Save the updated stock to the file

# Function to update stock quantity (restock or sell)
def update_stock():
    product_id = input("Enter Product ID: ").strip()
    if product_id not in stock:
        print("Product ID not found.")
        return

    print("\n\t\t\t\t\t-------------------------- Update Stock -----------------------\n")
    print("\t\t\t\t\t\t[1] Add Stock\t\t\t\t\t      ")
    print("\t\t\t\t\t\t[2] Reduce Stock\t\t\t\t\t      \n")
    print("\t\t\t\t\t---------------------------------------------------------------\n")

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
    
    print("\n\t\t\t\t\t-------------------------- View Stocks Option -----------------------------\n")
    print("[1] View All Products")
    print("[2] View by Category")
    print("\t\t\t\t\t---------------------------------------------------------------\n")

    choice = input("Enter your choice: ").strip()
    
    if choice == "1":
        print("\n\t\t\t\t\t-------------------------- Current Stock -----------------------\n")
        print(f"{'\t\t\t\t\tID':<10}{'\t\tName':<20}{'\tQuantity':<10}{'\tPrice':<10}{'Category':<15}")
        for product_id, details in stock.items():
            print(f"\t\t\t\t\t{product_id:<10}\t{details['name']:<20}\t {details['quantity']:<10}\t{details['price']:<10.2f}\t{details['category']:<15}")
        print("\t\t\t\t\t---------------------------------------------------------------\n")
    elif choice == "2":
        print("\nSelect Category:")
        print("1. Cleanser")
        print("2. Moisturizer")
        print("3. Serum")
        print("4. Sunscreen")
        category_choice = input("Enter your choice: ").strip()
        categories = {
            "1": "Cleanser",
            "2": "Moisturizer",
            "3": "Serum",
            "4": "Sunscreen"
        }
        category = categories.get(category_choice, None)
        if not category:
            print("Invalid category choice.")
            return

        print(f"\n\t\t\t\t\t-------------------------- Products in Category: {category} -----------------------")
        print(f"{'\t\t\t\t\tID':<10}{'\t\tName':<20}{'\tQuantity':<10}{'\tPrice':<10}")
        for product_id, details in stock.items():
            if details["category"] == category:
                print(f"\t\t\t\t\t{product_id:<10}\t{details['name']:<20}\t {details['quantity']:<10}\t{details['price']:<10.2f}")
        print("\t\t\t\t\t-------------------------------------------------------------------------\n")
    else:
        print("Invalid choice. Please try again.")
        
    # Function to searc for a product
def search_product():
    product_id = input("Enter Product ID to search: ").strip()
    if product_id not in stock:
        print("Product ID not found.")
        return
    details = stock[product_id]
    print("\n\t\t\t\t\t-------------------------- Product Details -----------------------\n")
    print(f"\t\t\t\t\tName: {details['name']}")
    print(f"\t\t\t\t\tQuantity: {details['quantity']}")
    print(f"\t\t\t\t\tPrice: {details['price']:.2f}")
    print(f"\t\t\t\t\tCategory: {details['category']}")
    print("\t\t\t\t\t---------------------------------------------------------------\n")

def main():
    load_stock()
    while True:
        print("\n\t\t\t\t\t\t\t -------------------------")
        print("\t\t\t\t\t\t\t| Stock Management System |")
        print("\t\t\t\t\t\t\t -------------------------")
        print("\n\t\t\t\t\t-------------------------- WATSON -----------------------------\n")
        print("\t\t\t\t\t\t[1] Add Product \t\t[2] Update Product   ")
        print("\t\t\t\t\t\t[3] View all Product \t\t[4] Search Product   ")
        print("\t\t\t\t\t\t[5] Exit\t\t\t\t\t      \n")
        print("\t\t\t\t\t---------------------------------------------------------------")
        choice = input("\t\t\t\t\t\nEnter your Choice: ").strip()
        
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
         
        