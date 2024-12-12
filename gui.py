import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from project import load_stock, save_stock, stock

def get_next_product_id():
    """Returns the next product ID by finding the highest current product ID and incrementing it."""
    if stock:
        max_id = max(int(product_id) for product_id in stock.keys())
        return str(max_id + 1)
    return "1"  # If no products exist, start from 1

def view_stock_gui():
    view_window = tk.Toplevel()
    view_window.title("View Products")
    view_window.geometry("1000x600")

    # Create a Treeview with columns including Product ID
    tree = ttk.Treeview(view_window, columns=("Product ID", "Name", "Quantity", "Price", "Category"), show="headings")
    
    # Define the headings for the columns
    tree.heading("Product ID", text="Product ID")
    tree.heading("Name", text="Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Category", text="Category")

    # Add the treeview/table to the window
    tree.pack(fill=tk.BOTH, expand=True)

    # Populate the Treeview/table with stock data, including Product ID
    for product_id, details in stock.items():
        tree.insert("", tk.END, values=(product_id, details["name"], details["quantity"], details["price"], details["category"]))


def add_product_gui():
    def generate_product_id():
        # Generate the next product ID
        existing_ids = [int(product_id) for product_id in stock.keys()]
        next_id = max(existing_ids, default=0) + 1  # Increment the highest ID
        return f"{next_id:03d}"  # Format it with leading zeros (e.g., 001, 002, ..., 300)

    def save_new_product():
        product_id = generate_product_id()  # Generate the next product ID
        name = name_entry.get().strip()
        try:
            quantity = int(quantity_entry.get().strip())
            price = float(price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please fill in all required info!")
            return
        
        # Ask for category
        category = category_entry.get().strip()
        if not category:
            response = messagebox.askyesno(
                "New Category",
                "No category was entered. Would you like to add a new category?"
            )
            if response:
                category = simpledialog.askstring("New Category", "Enter a new category:")
                if not category:  # User canceled or entered nothing
                    messagebox.showerror("Error", "Category is required.")
                    return
            else:
                messagebox.showerror("Error", "Category is required.")
                return
        
        # Save the new product
        stock[product_id] = {"name": name, "quantity": quantity, "price": price, "category": category}
        save_stock()
        messagebox.showinfo("Success", f"Product '{name}' added with Product ID {product_id}!")
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.geometry("500x300")
    add_window.title("Add Product")

    # Product ID (read-only)
    tk.Label(add_window, text="Product ID:").grid(row=0, column=0, padx=5, pady=5)
    product_id_entry = tk.Entry(add_window)
    product_id_entry.insert(0, generate_product_id())
    product_id_entry.config(state='readonly')
    product_id_entry.grid(row=0, column=2, padx=5, pady=5)

    # Product Name
    tk.Label(add_window, text="Name:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=1, column=3, padx=5, pady=5)

    # Quantity
    tk.Label(add_window, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
    quantity_entry = tk.Entry(add_window)
    quantity_entry.grid(row=2, column=3, padx=5, pady=5)

    # Price
    tk.Label(add_window, text="Price:").grid(row=3, column=0, padx=5, pady=5)
    price_entry = tk.Entry(add_window)
    price_entry.grid(row=3, column=3, padx=5, pady=5)

    # Category
    tk.Label(add_window, text="Category:").grid(row=4, column=0, padx=5, pady=5)
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=4, column=3, padx=5, pady=5)

    # Add Product Button
    tk.Button(add_window, text="Add Product", command=save_new_product).grid(row=5, column=2, columnspan=2, pady=10)

def search_product_gui():
    def perform_search():
        search_term = search_entry.get().strip()

        # Validate input: allow only letters and spaces
        if not search_term.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a valid search term!")
            return

        # Search for matching products
        search_term = search_term.lower()
        results_window = tk.Toplevel()
        results_window.title("Search Results")
        results_window.geometry("1000x600")

        # Create a Treeview for displaying search results
        tree = ttk.Treeview(results_window, columns=("Product ID", "Name", "Quantity", "Price", "Category"), show="headings")
        tree.heading("Product ID", text="Product ID")
        tree.heading("Name", text="Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Price", text="Price")
        tree.heading("Category", text="Category")
        tree.pack(fill=tk.BOTH, expand=True)

        # Populate the Treeview with results
        for product_id, details in stock.items():
            if (
                search_term in product_id.lower() or
                search_term in details["name"].lower() or
                search_term in details["category"].lower()
            ):
                tree.insert("", tk.END, values=(product_id, details["name"], details["quantity"], details["price"], details["category"]))

        # Display a message if no results are found
        if not tree.get_children():
            tk.Label(results_window, text="No results found.", fg="red").pack()

    # Create the search window
    search_window = tk.Toplevel()
    search_window.title("Search Product")
    search_window.geometry("500x200")

    tk.Label(search_window, text="Enter Product Name or Category (letters only):").pack(pady=10)
    search_entry = tk.Entry(search_window, width=30)
    search_entry.pack(pady=5)

    tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)

def update_product_gui():
    def display_all_products():
        """Populates the Treeview with all products."""
        tree.delete(*tree.get_children())  # Clear any existing rows
        for product_id, details in stock.items():
            tree.insert("", tk.END, values=(product_id, details["name"], details["quantity"], details["price"], details["category"]))

    def display_low_stock_products():
        """Populates the Treeview with products having stock < 10."""
        tree.delete(*tree.get_children())  # Clear any existing rows
        for product_id, details in stock.items():
            if details["quantity"] < 10:
                tree.insert("", tk.END, values=(product_id, details["name"], details["quantity"], details["price"], details["category"]))

        # Message if no products are found
        if not tree.get_children():
            messagebox.showinfo("Info", "No products with less than 10 quantity.")

    def select_product_to_update():
        """Handles the logic for updating the selected product."""
        # Get the selected product from the treeview
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to update!")
            return

        product_id = tree.item(selected_item, "values")[0]
        current_quantity = stock[product_id]["quantity"]

        # Ask the user if they want to add stock
        response = messagebox.askyesno(
            "Update Stock",
            f"Do you want to add stock to '{stock[product_id]['name']}'?\n"
            f"Current quantity: {current_quantity}"
        )

        if response:  # User clicked Yes
            try:
                add_quantity = simpledialog.askinteger(
                    "Enter Quantity",
                    "Enter the quantity to add:",
                    minvalue=1
                )
                if add_quantity is None:
                    return  # User canceled the input
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity entered!")
                return

            # Update the stock
            new_quantity = current_quantity + add_quantity

            # Save the updated stock
            stock[product_id]["quantity"] = new_quantity
            save_stock()
            messagebox.showinfo(
                "Success",
                f"{add_quantity} units were added to '{stock[product_id]['name']}'.\n"
                f"New stock quantity: {new_quantity}"
            )
            update_window.destroy()

        else:  # User clicked No
            reduce_response = messagebox.askyesno(
                "Reduce Stock",
                f"Do you want to reduce stock of '{stock[product_id]['name']}'?"
            )
            if not reduce_response:
                return  # Do nothing if they don't want to reduce stock

            try:
                reduce_quantity = simpledialog.askinteger(
                    "Enter Quantity",
                    f"Enter the quantity to reduce (current stock: {current_quantity}):",
                    minvalue=1
                )
                if reduce_quantity is None:
                    return  # User canceled the input
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity entered!")
                return

            if reduce_quantity > current_quantity:
                messagebox.showerror(
                    "Error",
                    "Cannot reduce stock by more than the current quantity!"
                )
                return

            # Update the stock
            new_quantity = current_quantity - reduce_quantity

            # Save the updated stock
            stock[product_id]["quantity"] = new_quantity
            save_stock()
            messagebox.showinfo(
                "Success",
                f"{reduce_quantity} units were deducted from '{stock[product_id]['name']}'.\n"
                f"New stock quantity: {new_quantity}"
            )
            update_window.destroy()

    # Create the update window
    update_window = tk.Toplevel()
    update_window.title("Update Products")
    update_window.geometry("1000x600")

    # Create a Treeview to show products
    tree = ttk.Treeview(update_window, columns=("Product ID", "Name", "Quantity", "Price", "Category"), show="headings")
    tree.heading("Product ID", text="Product ID")
    tree.heading("Name", text="Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Category", text="Category")
    tree.pack(fill=tk.BOTH, expand=True)

    # Display all products initially
    display_all_products()

    # Add buttons for filtering and updating
    button_frame = tk.Frame(update_window)
    button_frame.pack(fill=tk.X, pady=10)

    tk.Button(button_frame, text="Show All Products", command=display_all_products).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Show Low Stock Products", command=display_low_stock_products).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Update Selected Product", command=select_product_to_update).pack(side=tk.LEFT, padx=10)


def main_gui():
    load_stock()  # Load stock data when GUI starts

    root = tk.Tk()
    root.title("Stock Management System")
    root.geometry("400x300")

    tk.Button(root, text="View Stock", command=view_stock_gui).pack(pady=20)
    tk.Button(root, text="Add Product", command=add_product_gui).pack(pady=10)
    tk.Button(root, text="Search Product", command=search_product_gui).pack(pady=10)
    tk.Button(root, text="Update Product", command=update_product_gui).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
