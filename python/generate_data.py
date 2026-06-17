import random
import csv
from datetime import datetime, timedelta

categories = ['Electronics', 'Furniture', 'Office Supplies', 'Software', 'Accessories']
regions = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']
segments = ['enterprise', 'mid-market', 'small-biz']
statuses = ['delivered', 'pending', 'cancelled']
ticket_categories = ['billing', 'technical', 'shipping', 'account', 'product']
priorities = ['low', 'medium', 'high']


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

for customer_id in range(1,201):
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
        'total_amount': 0
    }
    orders.append(order)

print(orders[0])
print(orders[1])
print(f"Total orders created: {len(orders)}")

with open('data/orders.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=orders[0].keys())
    writer.writeheader()
    writer.writerows(orders)

print("Saved to data/orders.csv")

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

print(invoices[0])
print(invoices[1])
print(f"Total invoices created: {len(invoices)}")

with open('data/invoices.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=invoices[0].keys())
    writer.writeheader()
    writer.writerows(invoices)


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

print(tickets[0])
print(tickets[1])       
print(f"Total tickets created: {len(tickets)}")

with open('data/tickets.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=tickets[0].keys())
    writer.writeheader()
    writer.writerows(tickets)