# 📊 E-Commerce Data Analytics Platform

A desktop application for analyzing e-commerce data with an intuitive GUI built with Python and Tkinter. Features data visualization charts for sales and return trends.
As a personal development project, it is intended for technical learning and practice

> **Author:** [ZhenyuanYang-Frisk]  
> **Email:** [2230468051@qq.com]  
> **Year:** 2026

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Chart Functions](#-chart-functions)
- [Screenshots](#-screenshots)
- [Iteration Process](#-iteration-process)
- [Issues & Solutions](#-issues--solutions)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 📦 Order Analysis
- Multi-filter search: date range, order status, payment method, region
- Smart sorting: by date (newest/oldest) or order ID (largest/smallest)
- Order detail drill-down: view products, quantities, and price breakdown
- Automatic calculations: subtotal, discount amount, total paid
- Statistics: total orders, unique customers, region coverage

### 📋 Product Analysis
- Full catalog view with complete specifications
- Sort by launch date (newest/oldest)
- Search by `active_flag`

### 🔄 Return Analysis
- View all return records
- Sort by date or refund amount
- Return reason distribution statistics
- Daily return trend analysis
- Refund amount statistics (total, average, max, min)

### 📂 Category Analysis
- Dynamic category buttons loaded from database
- Click any category to view its products
- Cross-category product viewing

### 👤 Customer Analysis
- Fuzzy and exact name search
- Multi-dimension sorting: last name, customer type, city, province, country, signup date
- Distribution statistics: customer type, acquisition channel, province

### 📊 Data Visualization 
- **Sales Chart**: Daily sales revenue with order count overlay
- **Return Chart**: Daily refund amount with return count overlay
- **Sales vs Returns Chart**: Side-by-side comparison with trend analysis

### 🛠️ Common Features
- Interactive table sorting by any numeric column
- One-click CSV export
- Unrestricted data viewing (all rows displayed)
- Comprehensive error handling

---

## 🛠️ Tech Stack

| Category           | Technology         |
|--------------------|--------------------|
| Language           | Python 3.14+       |
| GUI Framework      | Tkinter            |
| Database Connector | PyMySQL 1.2.0+     |
| Data Processing    | Pandas 3.0.3+      |
| Data Visualization | Matplotlib 3.11+   |
| Database           | MySQL 5.7+         |
| Development Tools  | DataGrip / PyCharm |

---


## 📁 Project Structure

```
ecommerce-data-analytics
│
├── main.py                      # Main application entry point
├── config.py                    # Database configuration (create your own)
├── requirements.txt             # Python package dependencies
├── .gitignore                   # Git ignore rules
│
├── database                    # Database scripts
│   ├── schema.sql               # Complete table creation script
│   ├── sample_data.sql          # Sample test data
│   ├── queries.sql              # Useful SQL queries reference
│   └── README.md                # Database documentation
│
├── screenshots                 # Application screenshots
│   ├── 1_main_page.png          # Main dashboard
│   ├── 2_order_analysis.png     # Order analysis page
│   ├── 3_order_detail.png       # Order detail query window
│   ├── 4_order_results.png      # Order query results table
│   ├── 5_product_analysis.png   # Product analysis page
│   ├── 6_product_search.png     # Product search by flag
│   ├── 7_return_analysis.png    # Return analysis page
│   ├── 8_return_results.png     # Return analysis results
│   ├── 9_category_analysis.png  # Category analysis page
│   ├── 10_category_products.png # Category products display
│   ├── 11_customer_analysis.png # Customer analysis page
│   ├── 12_customer_search.png   # Customer search window
│   ├── 13_sales_chart.png       # Sales trend chart
│   └── 14_return_chart.png      # Return trend chart
│    
└── README.md                    # This file
```

---



## 🗄️ Database Design

The database consists of **7 core tables** that store all e-commerce data.

```
┌─────────────────┐          ┌─────────────────┐
│    regions      │          │   categories    │
│  region_id(PK)  │          │ category_id(PK) │
│  region_name    │          │  category_name  │
│  region_code    │          │   description   │
│  country        │          └─────────────────┘
└────────┬────────┘                    │
         │ 1                           │ 1
         │                             │
         │ N                           │ N
         │                    ┌────────┴────────┐
         │                    │    products     │
         │                    │  product_id(PK) │
         │                    │  category_id(FK)│
         │                    │   product_name  │
         │                    │   unit_cost     │
         │                    │   unit_price    │
         │                    │   launch_date   │
         │                    │   active_flag   │
         │                    └────────┬────────┘
         │                             │ 1
         │                             │
         │                             │ N
         │                    ┌────────┴────────┐
         │                    │   order_items   │
         │                    │order_item_id(PK)│
         │                    │   order_id(FK)  │
         │                    │  product_id(FK) │
         │                    │    quantity     │
         │                    │   discount_pct  │
         │                    │   item_price    │
         │                    └────────┬────────┘
         │                             │ 1
         │                             │
         │ N                           │ N
┌────────┴────────┐          ┌────────┴────────┐
│     orders      │          │    returns      │
│  order_id(PK)   │          │  return_id(PK)  │
│ customer_id(FK) │◀─────────│order_item_id(FK)│
│  region_id(FK)  │          │   return_date   │
│   order_date    │          │  return_reason  │
│  order_status   │          │  refund_amount  │
│ payment_method  │          └─────────────────┘
└────────┬────────┘
         │
         │ N
         │
┌────────┴────────┐
│   customers     │
│ customer_id(PK) │
│  region_id(FK)  │
│   first_name    │
│   last_name     │
│     email       │
│   signup_date   │
│  customer_type  │
│acquisition_channel│
│      city       │
│    province     │
│     country     │
└─────────────────┘
```


---

## 📥 Installation Guide

### Prerequisites

- Python 3.8+ installed
- MySQL 5.7+ installed and running
- DataGrip or similar SQL client (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce-data-analytics.git
cd ecommerce-data-analytics
```

### Step 2: Set Up the Database

1.Create database in DataGrip or MySQL CLI:
```sql
CREATE DATABASE e_commerce;
USE e_commerce;
```

2.Run the schema to create all tables:
```sql
SOURCE database/schema.sql;
```

3.Load sample data (optional):
```sql
SOURCE database/sample_data.sql;
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Connection
Create config.py in the project root:
```python
# config.py
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password_here',
    'database': 'e_commerce',
    'charset': 'utf8mb4'
}
```

### Step 5: Run the Application
```bash
python main.py
```

---

## 📖 Usage Guide

### Main Menu
Launch the application to see the main dashboard with five analysis modules and chart buttons.

### Order Analysis
1. **Filter**: Select date range, status, payment method, region

2. **Query**: Click "🔍 Query" to apply filters

3. **Order Detail**: Click "🔍 Query Order Detail" to view individual order breakdown

4. **View All**: Click "📋 View All" to display all orders

5. **Charts**: Click "📊 Show Sales Chart"

### Order Detail Calculation
| Field              | Formula        |
|--------------------|--------------------|
| Subtotal           | `quantity × unit_price`       |
| Discount Amount    | `quantity × unit_price × (discount_pct / 100)`          |
| Total Paid | `Subtotal - Discount Amount`           |
| Order Summary   | Sum of all items in the order       |

### Table Operations
**Sort**: Select a numeric column → Choose ascending/descending → Click "Apply Sort"

**Export**: Click "📥 Export CSV" to download current data

---

## 📊 Chart Functions
The application includes two data visualization charts that provide visual insights into business performance.

### Sales Chart
| Aspect          | Description       |
|-----------------|--------------------|
| Data Source | Calculated from `order_items` table      |
| Formula | `SUM(quantity × item_price × (1 - discount_pct / 100))` |
| Display | Line chart showing daily sales revenue + bar chart showing order count   |
| Access  | Main page / Order Analysis page       |
| Period  | Last 30 days   |
| Purpose | Visualize revenue trends and order volume patterns |

### Return Chart

| Aspect          | Description       |
|-----------------|--------------------|
| Data Source | Calculated from `returns` table     |
| Formula | `SUM(refund_amount)` |
| Display | Line chart showing daily refund amount + bar chart showing return count   |
| Access  | Main page / Return Analysis page       |
| Period  | Last 30 days   |
| Purpose | Track refund patterns and identify potential product quality issues |

## 📸 Screenshots
| Module	            | Screenshot                                   |
|--------------------|----------------------------------------------|
| Main Page          | https://screenshots/1_main_page.png          |
| Order Analysis     | https://screenshots/2_order_analysis.png     |
| Order Detail Query | https://screenshots/3_order_detail_query.png |
| Order Results      | https://screenshots/4_order_results.png      |
| Product Analysis   | https://screenshots/5_product_analysis.png   |
| Product Search     | https://screenshots/6_product_search.png     |
| Return Analysis    | https://screenshots/7_return_analysis.png    |
| Return Results     | https://screenshots/8_return_results.png     |
| Category Analysis  | https://screenshots/9_category_analysis.png  |
| Category Products  | https://screenshots/10_category_products.png |
| Customer Analysis  | https://screenshots/11_customer_analysis.png |
| Customer Search    | https://screenshots/12_customer_search.png   |
| Sales Chart        | https://screenshots/13_sales_chart.png       |
| Return Chart       | https://screenshots/14_return_chart.png      |

## 🔄 Iteration Process
### v1.0 - Foundation
MySQL connection and basic table display

Initial error handling

CSV import to MySQL

### v2.0 - Feature Expansion
Added 5 analysis modules: Orders, Products, Returns, Categories, Customers

Code modularization with query_data() and show_table_window()

UI layout optimization

### v3.0 - Enhancement
Order detail drill-down with price calculations

Customer search (fuzzy and exact)

Scrollbar support for long pages

Comprehensive error handling with user-friendly messages

### v4.0 - Data Visualization
**Sales Chart**: Daily sales trend with order count overlay

**Return Chart**: Daily return trend with return count overlay

Chart access from main page and relevant modules

### Key Design Decisions
| Decision       | Choice                      | Rationale                                         |
|----------------|-----------------------------|---------------------------------------------------|
| GUI Framework  | Tkinter                     | Python standard library, no extra installation    |
| Database       | MySQL                       | Popular relational database with DataGrip support |
| Data Display   | All rows, no pagination     | E-commerce data typically small (<10k rows)       |
| Chart Library  | Matplotlib                  | Integrates well with Tkinter, widely used         |
| Error Handling | Try-except + dialog boxes   | User-friendly, no console interaction needed      |

## ❓ Issues & Solutions
### Issue 1: DataGrip Only Shows 500 Rows
**Problem**: Sorting appears incorrect in DataGrip

**Cause**: DataGrip limits display to 500 rows by default

**Solution**: Click "No limit" in DataGrip's result window or view data in Python application

### Issue 2: Refund Amount Sorting Incorrect
**Problem**: `'10'` appears before `'9.99'` when sorting

**Cause**: Column stored as VARCHAR instead of DECIMAL

**Solution**: Use  `CAST(refund_amount AS DECIMAL(10,2))` in ORDER BY clause

### Issue 3: Customer Analysis Buttons Not Centered
**Problem**: Buttons aligned to left with scrollbar

**Cause**: Canvas default `anchor="nw"` (top-left)

**Solution**: Changed to `anchor="center"` with dynamic width binding

### Issue 4: NameError in Customer Search
**Problem**: `search_customer_window` function not found

**Cause**: Function called before definition

**Solution**: Move all standalone functions before the App class

## 📄 License

MIT License

Copyright (c) 2026 [Zhenyuan Yang]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 📞 Contact
GitHub: @ZhenyuanYang-Frisk

Email: 2230468051@qq.com

Project URL: https://github.com/ZhenyuanYang-Frisk/ecommerce-data-analytics.git