# SmartBiz Analytics Platform

> An end-to-end business intelligence platform built from scratch to simulate how real companies use ERP data for decision-making. SQL · Python · Power BI

---

## The Problem

ERP systems like Odoo are excellent at running day-to-day operations — orders, invoices, inventory, support — but they don't always surface the insights leadership actually needs. During my Business Systems Analyst internship at Odoo, I saw this gap firsthand: companies had all the data, but no analytical layer turning it into decisions.

This project is my attempt to build that missing layer.

---

## What's Inside

**1. SQL Database**
A 6-table relational schema modeling a realistic mid-size business:
- `customers` — 200 simulated companies across 5 regions and 3 segments
- `products` — 50 products across 5 categories
- `orders` and `order_items` — 500 orders with realistic delivery timelines (including early and late deliveries)
- `invoices` — 600 invoices with payment status logic (paid, pending, overdue)
- `support_tickets` — 300 tickets with category, priority, and resolution tracking

15+ business analysis queries answering real operational questions: revenue trends, on-time delivery rates, overdue invoices by segment, top products, customer lifetime value, and more.

**2. Python Data Generation & Modeling**
All data is generated programmatically using Python (`random`, `datetime`) to create realistic, internally consistent relationships across tables — for example, invoice due dates that logically follow issue dates, and delivery dates that sometimes run early and sometimes late.

Predictive models built with Pandas and scikit-learn:
- Customer churn risk scoring
- Late invoice payment prediction
- Inventory stockout alerts

**3. Power BI Dashboard**
A multi-page executive dashboard covering:
- Executive Overview (revenue, order volume, trends)
- Operations Health (delivery performance)
- Customer Intelligence (churn risk, segment analysis)
- Financial Pulse (invoice and payment status)
- Inventory Watch (stock levels and reorder alerts)

---

## Tech Stack

Python · Pandas · scikit-learn · SQLite · Power BI · Git/GitHub

---

## Status

In progress — built as part of a self-directed summer learning plan (June–August 2026).

**Phase 1 — Complete ✅**
- 6-table relational database designed and built in SQLite
- 2,643 records generated across all tables using Python
- Full data generation script (generate_data.py) with realistic conditional logic

**Phase 2 — In Progress 🔄**
- 15+ SQL business analysis queries
- Python predictive models (churn, late payments, stockout alerts)
- Power BI executive dashboard (5 pages)

---

## How to Run

1. Clone this repo
2. Run `python python/generate_data.py` to generate all datasets
3. Open `data/smartbiz.db` in DB Browser for SQLite to explore the database
4. Run queries from `sql/business_queries.sql`
5. Power BI dashboard file coming soon

---

*Built by Rishit Garg | [LinkedIn](https://www.linkedin.com/in/garg-rishit)*