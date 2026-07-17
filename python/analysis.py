import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ============================================
# 1. DATABASE CONNECTION
# ============================================
# Connect to SmartBiz SQLite database and load all 6 tables into Pandas DataFrames

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

# ============================================
# 2. EXPLORATORY DATA ANALYSIS
# ============================================
# Quick overview of customer data structure and distribution

print("\n--- Customer Data Overview ---")
print(customers.head())
print(customers.dtypes)

# Distribution of customers across segments and regions
print("\nCustomers per segment:")
print(customers['segment'].value_counts())

print("\nCustomers per region:")
print(customers['region'].value_counts())

# ============================================
# 3. CHURN RISK MODEL
# ============================================
# Predict which customers are at risk of churning
# A customer is defined as churned if they haven't ordered in 180+ days

# --- Feature Engineering ---

# Find most recent order date per customer -- key signal for churn
last_order = orders.groupby('customer_id')['order_date'].max().reset_index()
last_order.columns = ['customer_id', 'last_order_date']
last_order['last_order_date'] = pd.to_datetime(last_order['last_order_date'])

# Calculate how many days ago each customer last ordered
last_order['days_since_order'] = (pd.Timestamp('today') - last_order['last_order_date']).dt.days

# Count total orders per customer -- frequency signal
order_counts = orders.groupby('customer_id')['order_id'].count().reset_index()
order_counts.columns = ['customer_id', 'total_orders']

# Calculate total spend per customer -- monetary signal
total_spend = orders.groupby('customer_id')['total_amount'].sum().reset_index()
total_spend.columns = ['customer_id', 'total_spend']

# Merge all features into one customer feature table
features = customers[['customer_id', 'segment', 'region']].copy()
features = features.merge(last_order, on='customer_id', how='left')
features = features.merge(order_counts, on='customer_id', how='left')
features = features.merge(total_spend, on='customer_id', how='left')

# Create churn label -- 1 = churned, 0 = active
features['churned'] = (features['days_since_order'] >= 180).astype(int)

print(f"\nChurned customers: {features['churned'].sum()}")
print(f"Active customers: {(features['churned'] == 0).sum()}")

# --- Model Training ---

# Encode categorical variables -- ML models require numbers not text
le_segment = LabelEncoder()
le_region = LabelEncoder()
features['segment_encoded'] = le_segment.fit_transform(features['segment'])
features['region_encoded'] = le_region.fit_transform(features['region'])

# Replace any missing values with 0
features = features.fillna(0)

# Define inputs (X) and target (y)
X = features[['days_since_order', 'total_orders', 'total_spend',
               'segment_encoded', 'region_encoded']]
y = features['churned']

# Split 80% training, 20% testing -- keeps test set unseen during training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining on {len(X_train)} customers")
print(f"Testing on {len(X_test)} customers")

# Train RandomForest -- builds 100 decision trees and takes majority vote
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate accuracy on unseen test data
accuracy = model.score(X_test, y_test)
print(f"Churn model accuracy: {round(accuracy * 100, 1)}%")

# Score all 200 customers with churn probability (0 = safe, 1 = certain churn)
features['churn_risk_score'] = model.predict_proba(X)[:, 1]

# Export top 20 highest risk customers for sales team action
top_churn = features[['customer_id', 'segment', 'region',
                        'days_since_order', 'total_orders',
                        'total_spend', 'churn_risk_score']].sort_values(
                        'churn_risk_score', ascending=False).head(20)

print("\nTop 20 customers at highest churn risk:")
print(top_churn.to_string())

top_churn.to_csv('data/churn_risk_customers.csv', index=False)
print("Saved churn results to data/churn_risk_customers.csv")

# --- Feature Importance ---
# Shows which inputs the model relied on most to make predictions
feature_names = ['days_since_order', 'total_orders', 'total_spend',
                 'segment_encoded', 'region_encoded']
importances = model.feature_importances_

print("\nFeature importance scores:")
for name, score in zip(feature_names, importances):
    print(f"  {name}: {round(score, 3)}")

# --- Churn Score Visualization ---
# Histogram showing distribution of churn risk across all 200 customers
plt.figure(figsize=(10, 6))
sns.histplot(features['churn_risk_score'], bins=20, color='red')
plt.title('Customer Churn Risk Score Distribution')
plt.xlabel('Churn Risk Score (0 = Safe, 1 = High Risk)')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('data/churn_distribution.png')
plt.show()
print("Churn distribution chart saved!")

# ============================================
# 4. LATE INVOICE PREDICTOR
# ============================================
# Predict which invoices are likely to be paid late
# Uses invoice amount and customer segment/region as features

# --- Feature Engineering ---

# Link invoices to customer segment/region via orders table
# invoices -> orders -> customers (two step join)
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

# Convert date columns from text to datetime for comparison
invoice_features['paid_date'] = pd.to_datetime(invoice_features['paid_date'], errors='coerce')
invoice_features['due_date'] = pd.to_datetime(invoice_features['due_date'], errors='coerce')

# Create late payment label -- 1 = paid after due date, 0 = on time or unpaid
invoice_features['paid_late'] = (
    invoice_features['paid_date'] > invoice_features['due_date']
).astype(int)

print(f"\nLate payments: {invoice_features['paid_late'].sum()}")
print(f"On time/unpaid: {(invoice_features['paid_late'] == 0).sum()}")

# --- Model Training ---

# Encode categorical variables
le_segment = LabelEncoder()
le_region = LabelEncoder()
invoice_features['segment_encoded'] = le_segment.fit_transform(
    invoice_features['segment'].fillna('unknown'))
invoice_features['region_encoded'] = le_region.fit_transform(
    invoice_features['region'].fillna('unknown'))
invoice_features['amount'] = invoice_features['amount'].fillna(0)

# Define inputs and target
X_inv = invoice_features[['amount', 'segment_encoded', 'region_encoded']]
y_inv = invoice_features['paid_late']

# Split 80/20 train/test
X_train_inv, X_test_inv, y_train_inv, y_test_inv = train_test_split(
    X_inv, y_inv, test_size=0.2, random_state=42)

# Train RandomForest on invoice data
model_inv = RandomForestClassifier(n_estimators=100, random_state=42)
model_inv.fit(X_train_inv, y_train_inv)

accuracy_inv = model_inv.score(X_test_inv, y_test_inv)
print(f"Invoice model accuracy: {round(accuracy_inv * 100, 1)}%")

# Score all invoices with late payment probability
invoice_features['late_payment_risk'] = model_inv.predict_proba(X_inv)[:, 1]

# Export top 20 highest risk invoices for finance team to prioritize
high_risk = invoice_features[['invoice_id', 'amount', 'segment',
                               'late_payment_risk']].sort_values(
                               'late_payment_risk', ascending=False).head(20)

print("\nTop 20 high risk invoices:")
print(high_risk.to_string())

high_risk.to_csv('data/late_payment_risk.csv', index=False)
print("Saved to data/late_payment_risk.csv")

# ============================================
# 5. STOCKOUT ALERT SYSTEM
# ============================================
# Identify products at risk of running out of stock
# based on current inventory levels and historical sales velocity

# --- Calculate Sales Velocity ---

# Total units sold per product across all orders
daily_sales = order_items.groupby('product_id')['quantity'].sum().reset_index()
daily_sales.columns = ['product_id', 'total_units_sold']

# Merge sales data with product info -- LEFT JOIN keeps products never ordered
stockout = products.merge(daily_sales, on='product_id', how='left')
stockout['total_units_sold'] = stockout['total_units_sold'].fillna(0)

# Calculate average daily sales rate (data spans ~700 days)
stockout['avg_daily_sales'] = stockout['total_units_sold'] / 700

# Days of stock remaining = current stock / daily sales rate
# Products with zero sales get 999 days (no risk) to avoid division by zero
stockout['days_of_stock'] = stockout.apply(
    lambda row: row['stock_quantity'] / row['avg_daily_sales']
    if row['avg_daily_sales'] > 0 else 999,
    axis=1
)

# --- Risk Classification ---
# CRITICAL = under 30 days, WARNING = under 60 days, OK = 60+ days
stockout['risk_level'] = stockout['days_of_stock'].apply(
    lambda x: 'CRITICAL' if x < 30 else ('WARNING' if x < 60 else 'OK')
)

# Show only critical products sorted by most urgent first
critical = stockout[stockout['risk_level'] == 'CRITICAL'][
    ['name', 'category', 'stock_quantity', 'reorder_level',
     'days_of_stock', 'risk_level']
].sort_values('days_of_stock')

print(f"\nCritical stockout alerts: {len(critical)}")
print(critical.to_string())

stockout.to_csv('data/stockout_alerts.csv', index=False)
print("Saved to data/stockout_alerts.csv")

# ============================================
# 6. EXPORT DATA FOR POWER BI DASHBOARD
# ============================================
# Export SQL query results as CSVs for Power BI consumption

# Monthly revenue trend for executive overview page
monthly_revenue = pd.read_sql('''
    SELECT strftime('%Y-%m', order_date) AS month,
           SUM(total_amount) AS total_revenue,
           COUNT(order_id) AS total_orders
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
    ORDER BY month
''', conn)

monthly_revenue.to_csv('data/monthly_revenue.csv', index=False)
print("\nExported monthly_revenue.csv for Power BI")

print("\nAll analysis complete!")