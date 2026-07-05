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