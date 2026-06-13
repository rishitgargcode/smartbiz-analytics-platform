import random
import csv

categories = ['Electronics', 'Furniture', 'Office Supplies', 'Software', 'Accessories']

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