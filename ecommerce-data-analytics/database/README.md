# Database Schema: E-Commerce Data Analytics

## Overview
This database stores e-commerce data for the Data Analytics Platform.

## Tables

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `regions` | Geographic regions | region_id, region_name, country |
| `customers` | Customer information | customer_id, first_name, last_name, email |
| `categories` | Product categories | category_id, category_name |
| `products` | Product catalog | product_id, product_name, unit_price |
| `orders` | Order headers | order_id, customer_id, order_date |
| `order_items` | Order line items | order_item_id, order_id, product_id, quantity |
| `returns` | Return records | return_id, order_item_id, refund_amount |


## Setup Instructions

### 1. Create Database
```sql
CREATE DATABASE e_commerce;
USE e_commerce;
```
### 2. Run Schema
```bash
mysql -u root -p e_commerce < database/schema.sql
```

### 3. Load Sample Data
```bash
mysql -u root -p e_commerce < database/sample_data.sql
```

### 4. Verify Installation
```sql
SHOW TABLES;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM orders;
```


## Key Relationships
`orders` → `customers` (many-to-one)

`orders` → `regions` (many-to-one)

`order_items` → `orders` (many-to-one)

`order_items` → `products` (many-to-one)

`products` → `categories` (many-to-one)

`returns` → `order_items` (many-to-one)

## Indexes Created
`idx_orders_customer_id`, `idx_orders_order_date`, `idx_orders_status`

`idx_order_items_order_id`, `idx_order_items_product_id`

`idx_returns_order_item_id`, `idx_returns_return_date`

`idx_products_category_id`, `idx_products_active_flag`

`idx_customers_region_id`, `idx_customers_signup_date`

## Sample Queries
See `queries.sql` for useful analysis queries.
```
database/
├── schema.sql # build database (key)
├── sample_data.sql # sample data (Recommend)
├── queries.sql # common search (refer)
└── README.md # Database description (text)
```