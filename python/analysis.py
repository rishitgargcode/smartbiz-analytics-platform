import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('sql/smartbiz.db')

customers = pd.read_sql('SELECT * FROM customers', conn)
products = pd.read_sql('SELECT * FROM products', conn)
orders = pd.read_sql('SELECT * FROM orders', conn)
order_items = pd.read_sql('SELECT * FROM order_items', conn)
invoices = pd.read_sql('SELECT * FROM invoices', conn)
tickets = pd.read_sql('SELECT * FROM tickets', conn)

print("Tables loaded!")
print(f"Customers: {len(customers)} rows")
print(f"Products: {len(products)} rows")
print(f"Orders: {len(orders)} rows")
print(f"Order items: {len(order_items)} rows")
print(f"Invoices: {len(invoices)} rows")
print(f"Tickets: {len(tickets)} rows")

# What does our customer data look like?
print(customers.head())
print(customers.dtypes)

# How many customers per segment?
print(customers['segment'].value_counts())

# How many customers per region?
print(customers['region'].value_counts())