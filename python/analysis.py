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

last_order = orders.groupby('customer_id')['order_date'].max().reset_index()
last_order.columns = ['customer_id', 'last_order_date']
last_order['last_order_date'] = pd.to_datetime(last_order['last_order_date'])
last_order['days_since_order'] = (pd.Timestamp('today') - last_order['last_order_date']).dt.days

order_counts = orders.groupby('customer_id')['order_id'].count().reset_index()
order_counts.columns = ['customer_id', 'total_orders']

total_spend = orders.groupby('customer_id')['total_amount'].sum().reset_index()
total_spend.columns = ['customer_id', 'total_spend']

features = customers[['customer_id', 'segment', 'region']].copy()
features = features.merge(last_order, on='customer_id', how='left')
features = features.merge(order_counts, on='customer_id', how='left')
features = features.merge(total_spend, on='customer_id', how='left')

features['churned'] = (features['days_since_order'] >= 180).astype(int)

print(features.head(10))
print(f"\nChurned customers: {features['churned'].sum()}")
print(f"Active customers: {(features['churned'] == 0).sum()}")


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

le_segment = LabelEncoder()
le_region = LabelEncoder()
features['segment_encoded'] = le_segment.fit_transform(features['segment'])
features['region_encoded'] = le_region.fit_transform(features['region'])

features = features.fillna(0)

X = features[['days_since_order', 'total_orders', 'total_spend', 
               'segment_encoded', 'region_encoded']]
y = features['churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training on {len(X_train)} customers")
print(f"Testing on {len(X_test)} customers")

# Train the model (builds 100 decision trees)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#Test accuracy
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {round(accuracy * 100, 1)}%")

# Score ALL customers with churn probability
features['churn_risk_score'] = model.predict_proba(X)[:, 1]

top_churn = features[['customer_id', 'segment', 'region', 
                        'days_since_order', 'total_orders', 
                        'total_spend', 'churn_risk_score']].sort_values(
                        'churn_risk_score', ascending=False).head(20)

print("\nTop 20 customers at highest churn risk:")
print(top_churn.to_string())


top_churn.to_csv('data/churn_risk_customers.csv', index=False)
print("Saved churn results to data/churn_risk_customers.csv")


import matplotlib.pyplot as plt

feature_names = ['days_since_order', 'total_orders', 'total_spend', 
                 'segment_encoded', 'region_encoded']
importances = model.feature_importances_

for name, score in zip(feature_names, importances):
    print(f"{name}: {round(score, 3)}")

#Visualize
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.histplot(features['churn_risk_score'], bins=20, color='red')
plt.title('Customer Churn Risk Score Distribution')
plt.xlabel('Churn Risk Score')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('data/churn_distribution.png')
plt.show()
print("Chart saved!")

# LATE INVOICE PREDICTOR
invoice_features = invoices.merge(
    orders[['order_id', 'customer_id']], 
    on='order_id', 
    how='left'
)
invoice_features = invoice_features.merge(
    customers[['customer_id', 'segment', 'region']], 
    on='customer_id', 
    how='left'
)

invoice_features['paid_date'] = pd.to_datetime(invoice_features['paid_date'], errors='coerce')
invoice_features['due_date'] = pd.to_datetime(invoice_features['due_date'], errors='coerce')

invoice_features['paid_late'] = (
    invoice_features['paid_date'] > invoice_features['due_date']
).astype(int)

print(f"Late payments: {invoice_features['paid_late'].sum()}")
print(f"On time payments: {(invoice_features['paid_late'] == 0).sum()}")

# Step 3: Prepare features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

le_segment = LabelEncoder()
le_region = LabelEncoder()

invoice_features['segment_encoded'] = le_segment.fit_transform(
    invoice_features['segment'].fillna('unknown'))
invoice_features['region_encoded'] = le_region.fit_transform(
    invoice_features['region'].fillna('unknown'))
invoice_features['amount'] = invoice_features['amount'].fillna(0)

X_inv = invoice_features[['amount', 'segment_encoded', 'region_encoded']]
y_inv = invoice_features['paid_late']

X_train_inv, X_test_inv, y_train_inv, y_test_inv = train_test_split(
    X_inv, y_inv, test_size=0.2, random_state=42)


model_inv = RandomForestClassifier(n_estimators=100, random_state=42)
model_inv.fit(X_train_inv, y_train_inv)

accuracy_inv = model_inv.score(X_test_inv, y_test_inv)
print(f"Invoice model accuracy: {round(accuracy_inv * 100, 1)}%")


invoice_features['late_payment_risk'] = model_inv.predict_proba(X_inv)[:, 1]
high_risk = invoice_features[['invoice_id', 'amount', 'segment', 
                               'late_payment_risk']].sort_values(
                               'late_payment_risk', ascending=False).head(20)
print("\nTop 20 high risk invoices:")
print(high_risk.to_string())

high_risk.to_csv('data/late_payment_risk.csv', index=False)
print("Saved to data/late_payment_risk.csv")

# STOCKOUT ALERTS

daily_sales = order_items.groupby('product_id')['quantity'].sum().reset_index()
daily_sales.columns = ['product_id', 'total_units_sold']

stockout = products.merge(daily_sales, on='product_id', how='left')
stockout['total_units_sold'] = stockout['total_units_sold'].fillna(0)

stockout['avg_daily_sales'] = stockout['total_units_sold'] / 700
stockout['days_of_stock'] = stockout.apply(
    lambda row: row['stock_quantity'] / row['avg_daily_sales'] 
    if row['avg_daily_sales'] > 0 else 999,
    axis=1
)

stockout['risk_level'] = stockout['days_of_stock'].apply(
    lambda x: 'CRITICAL' if x < 30 else ('WARNING' if x < 60 else 'OK')
)

critical = stockout[stockout['risk_level'] == 'CRITICAL'][
    ['name', 'category', 'stock_quantity', 'reorder_level', 
     'days_of_stock', 'risk_level']
].sort_values('days_of_stock')

print(f"\nCritical stockout alerts: {len(critical)}")
print(critical.to_string())

stockout.to_csv('data/stockout_alerts.csv', index=False)
print("Saved to data/stockout_alerts.csv")