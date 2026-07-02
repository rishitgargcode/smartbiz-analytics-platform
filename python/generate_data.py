import random
import csv
from datetime import datetime, timedelta

categories = ['Electronics', 'Furniture', 'Office Supplies', 'Software', 'Accessories']
regions = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']
segments = ['enterprise', 'mid-market', 'small-biz']
statuses = ['delivered', 'pending', 'cancelled']
ticket_categories = ['billing', 'technical', 'shipping', 'account', 'product']
priorities = ['low', 'medium', 'high']

# PRODUCTS
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

with open('data/products.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=products[0].keys())
    writer.writeheader()
    writer.writerows(products)
print(f"Products: {len(products)} rows saved")

# CUSTOMERS
customers = []
for customer_id in range(1, 201):
    customer = {
        'customer_id': customer_id,
        'name': f'Company_{customer_id}',
        'email': f'contact{customer_id}@company{customer_id}.com',
        'region': random.choice(regions),
        'signup_date': (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))).strftime('%Y-%m-%d'),
        'segment': random.choice(segments)
    }
    customers.append(customer)

with open('data/customers.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)
print(f"Customers: {len(customers)} rows saved")

# ORDER ITEMS FIRST (so we can calculate order totals)
order_items = []
item_id = 1
order_totals = {}  # stores total_amount per order_id

for order_id in range(1, 501):
    num_items = random.randint(1, 3)
    order_total = 0
    
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = product['unit_price']
        order_total += quantity * unit_price
        
        order_item = {
            'item_id': item_id,
            'order_id': order_id,
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': unit_price
        }
        order_items.append(order_item)
        item_id += 1
    
    order_totals[order_id] = round(order_total, 2)

with open('data/order_items.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=order_items[0].keys())
    writer.writeheader()
    writer.writerows(order_items)
print(f"Order items: {len(order_items)} rows saved")

# ORDERS (now with real total_amount)
orders = []
for order_id in range(1, 501):
    order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
    expected_delivery = order_date + timedelta(days=random.randint(3, 10))
    actual_delivery = expected_delivery + timedelta(days=random.randint(-2, 5))
    
    order = {
        'order_id': order_id,
        'customer_id': random.randint(1, 200),
        'order_date': order_date.strftime('%Y-%m-%d'),
        'expected_delivery': expected_delivery.strftime('%Y-%m-%d'),
        'actual_delivery': actual_delivery.strftime('%Y-%m-%d'),
        'status': random.choice(statuses),
        'total_amount': order_totals[order_id]
    }
    orders.append(order)

with open('data/orders.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=orders[0].keys())
    writer.writeheader()
    writer.writerows(orders)
print(f"Orders: {len(orders)} rows saved")

# INVOICES
invoices = []
for invoice_id in range(1, 601):
    issue_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
    due_date = issue_date + timedelta(days=30)
    status = random.choice(['paid', 'overdue', 'pending'])
    
    if status == 'paid':
        paid_date = (issue_date + timedelta(days=random.randint(1, 35))).strftime('%Y-%m-%d')
    else:
        paid_date = ''
    
    invoice = {
        'invoice_id': invoice_id,
        'order_id': random.randint(1, 500),
        'issue_date': issue_date.strftime('%Y-%m-%d'),
        'due_date': due_date.strftime('%Y-%m-%d'),
        'paid_date': paid_date,
        'amount': round(random.uniform(20, 2000), 2),
        'status': status
    }
    invoices.append(invoice)

with open('data/invoices.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=invoices[0].keys())
    writer.writeheader()
    writer.writerows(invoices)
print(f"Invoices: {len(invoices)} rows saved")

# TICKETS
tickets = []
for ticket_id in range(1, 301):
    created_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
    status = random.choice(['open', 'closed', 'pending'])
    
    if status == 'closed':
        resolved_date = (created_date + timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d')
    else:
        resolved_date = ''
    
    ticket = {
        'ticket_id': ticket_id,
        'customer_id': random.randint(1, 200),
        'created_date': created_date.strftime('%Y-%m-%d'),
        'resolved_date': resolved_date,
        'category': random.choice(ticket_categories),
        'priority': random.choice(priorities),
        'status': status
    }
    tickets.append(ticket)

with open('data/tickets.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=tickets[0].keys())
    writer.writeheader()
    writer.writerows(tickets)
print(f"Tickets: {len(tickets)} rows saved")

print("\nAll done! Total records:")
print(f"  Products: {len(products)}")
print(f"  Customers: {len(customers)}")
print(f"  Order items: {len(order_items)}")
print(f"  Orders: {len(orders)}")
print(f"  Invoices: {len(invoices)}")
print(f"  Tickets: {len(tickets)}")