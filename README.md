                                                        STOCK MANAGEMENT SYSTEM 
                                                                Watson

VIDEO DEMO URL: https://youtu.be/GA4jPWGWmpk?si=S0kG96hW7DOLdRrp
DESCRIPTION:
A STOCK MANAGEMENT SYSTEM IS A SYSTEM THAT IS USED TO MONITOR, CONTROL, AND ORGANIZE THE INVENTORY OR STOCK LEVELS OF A BUSINESS. IT ENSURES THAT THERES IS A BALANCE BETWEEN THE STOCKS AVAILABLE AND THE BUSINESS OPERATIONAL NEEDS, REDUCING OVERSTOCKING, UNDERSTOCKING, AND WASTAGE. 

load_stock() : load existing stock data from the stock_data.csv file intoo the progra when it starts. it reads the details such as the product ID, name, quantity, price, and catagory. this key features ensures the system starts with the latest saved data.

saved_stock() : writes the current stock data to stock_data.csv to ensure changes are persistent. just like the load_stock saves all stocks details, including productID, name, quantity, price, category.

add_product() : allows the user to add new product to the stocks. prompts the user to input product details such as ID, name, quantity, price, and category. it ensure that the product ID is unique.

update_stock() : it updates the stocks level of an existing product. it allows the users to either add stock or reduce stock.

view_stock() : display the current stocks in different ways for better overview and management. theres an option to view all product and view product by category.

seach_product() : allows the user to loop up details of a specific product using its IDs. Displays detailed information about the product, such as name, quantity, price and category.

main() : it serves as the interfaces for the users interact with the system. the display menu with options to add product, update stock, view all stock, search for a product, exit the system. 

sys.exit() : it provides a clean way to close the program. it exits the system safely after saving all changes to the CSV file.
