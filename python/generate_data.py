import random
import csv
from datetime import datetime, timedelta

categories = ['Electronics', 'Furniture', 'Office Supplies', 'Software', 'Accessories']
regions = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']
segments = ['enterprise', 'mid-market', 'small-biz']

products = []

for product_id in range(1, 51):
    product = {
        'product_id': product_id,
        'name': f'Product_{product_id}',
        'category': random.choice(categories),
        'unit_price': round(random.uniform(5, 500), 2),
        'reorder_level': random.randint(10, 50),
        'stock_quantity': random.randint(0, 200)
    }
    products.append(product)

print(products[0])
print(products[1])
print(f"Total products created: {len(products)}")


with open('data/products.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=products[0].keys())
    writer.writeheader()
    writer.writerows(products)

print("Saved to data/products.csv")

customers = []

for customer_id in  range(1,201):
    customer = {
        'customer_id': customer_id,
        'name': f'Company_{customer_id}',
        'email': f'contact{customer_id}@company{customer_id}.com',
        'region': random.choice(regions),
        'signup_date': (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))).strftime('%Y-%m-%d'),
        'segment': random.choice(segments)
    }
    customers.append(customer)

print(customers[0])
print(customers[1])
print(f"Total customers created: {len(customers)}")

with open('data/customers.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

print("Saved to data/customers.csv")