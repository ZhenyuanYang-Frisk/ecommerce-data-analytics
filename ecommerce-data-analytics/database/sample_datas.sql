-- =============================================
-- Sample Data for E-Commerce Database
-- =============================================

-- Insert Regions
INSERT INTO regions (region_id, region_name, region_code, country) VALUES
(1, 'North America', 'NA', 'USA'),
(2, 'Europe', 'EU', 'UK'),
(3, 'Asia Pacific', 'APAC', 'China'),
(4, 'Latin America', 'LATAM', 'Brazil'),
(5, 'Middle East', 'ME', 'UAE');

-- Insert Categories
INSERT INTO categories (category_id, category_name, description) VALUES
(1, 'Electronics', 'Electronic devices and accessories'),
(2, 'Clothing', 'Apparel and fashion items'),
(3, 'Home & Kitchen', 'Home appliances and kitchenware'),
(4, 'Books', 'Books and publications'),
(5, 'Toys & Games', 'Children toys and games'),
(6, 'Sports', 'Sports equipment and gear'),
(7, 'Beauty', 'Beauty and personal care products'),
(8, 'Automotive', 'Car parts and accessories');

-- Insert Customers
INSERT INTO customers (customer_id, first_name, last_name, email, signup_date, customer_type, acquisition_channel, city, province, country, region_id) VALUES
(1, 'John', 'Smith', 'john.smith@email.com', '2023-01-15', 'Premium', 'Social Media', 'New York', 'NY', 'USA', 1),
(2, 'Emma', 'Johnson', 'emma.j@email.com', '2023-02-20', 'Regular', 'Referral', 'Los Angeles', 'CA', 'USA', 1),
(3, 'Michael', 'Brown', 'mike.brown@email.com', '2023-03-10', 'Premium', 'Search Engine', 'Chicago', 'IL', 'USA', 1),
(4, 'Sarah', 'Williams', 'sarah.w@email.com', '2023-04-05', 'Regular', 'Email Marketing', 'Houston', 'TX', 'USA', 1),
(5, 'David', 'Jones', 'david.jones@email.com', '2023-05-12', 'VIP', 'Social Media', 'Phoenix', 'AZ', 'USA', 1),
(6, 'Emily', 'Davis', 'emily.davis@email.com', '2023-06-18', 'Regular', 'Referral', 'Philadelphia', 'PA', 'USA', 1),
(7, 'James', 'Miller', 'james.miller@email.com', '2023-07-22', 'Premium', 'Search Engine', 'San Antonio', 'TX', 'USA', 1),
(8, 'Jessica', 'Wilson', 'jessica.w@email.com', '2023-08-30', 'Regular', 'Social Media', 'San Diego', 'CA', 'USA', 1),
(9, 'Robert', 'Moore', 'robert.moore@email.com', '2023-09-14', 'VIP', 'Email Marketing', 'Dallas', 'TX', 'USA', 1),
(10, 'Lisa', 'Taylor', 'lisa.taylor@email.com', '2023-10-01', 'Regular', 'Referral', 'London', 'England', 'UK', 2);

-- Insert Products
INSERT INTO products (product_id, product_name, category_id, unit_cost, unit_price, launch_date, active_flag) VALUES
(1, 'iPhone 15 Pro', 1, 800.00, 999.99, '2023-09-22', 'Active'),
(2, 'Samsung Galaxy S24', 1, 700.00, 899.99, '2024-01-17', 'Active'),
(3, 'Sony Headphones WH-1000XM5', 1, 250.00, 399.99, '2023-05-15', 'Active'),
(4, 'Apple Watch Series 9', 1, 350.00, 499.99, '2023-09-22', 'Active'),
(5, 'Levi\'s Jeans', 2, 40.00, 69.99, '2023-01-10', 'Active'),
(6, 'Nike Air Max', 2, 120.00, 199.99, '2023-03-01', 'Active'),
(7, 'North Face Jacket', 2, 150.00, 249.99, '2023-10-01', 'Active'),
(8, 'KitchenAid Mixer', 3, 300.00, 449.99, '2023-08-15', 'Active'),
(9, 'Instant Pot Duo', 3, 80.00, 129.99, '2023-06-01', 'Active'),
(10, 'The Great Gatsby (Book)', 4, 10.00, 19.99, '2023-01-01', 'Active'),
(11, 'Harry Potter Box Set', 4, 50.00, 79.99, '2023-02-01', 'Active'),
(12, 'Lego City Set', 5, 30.00, 49.99, '2023-07-15', 'Active'),
(13, 'Nerf Blaster', 5, 20.00, 34.99, '2023-09-01', 'Active'),
(14, 'Wilson Tennis Racket', 6, 150.00, 219.99, '2023-04-01', 'Active'),
(15, 'Yoga Mat', 6, 25.00, 39.99, '2023-05-01', 'Active'),
(16, 'Dyson Hair Dryer', 7, 300.00, 499.99, '2023-11-01', 'Active'),
(17, 'Car Dash Camera', 8, 60.00, 99.99, '2023-12-01', 'Active');

-- Insert Orders
INSERT INTO orders (order_id, customer_id, order_date, region_id, order_status, payment_method) VALUES
(1, 1, '2023-01-16 10:30:00', 1, 'Completed', 'Credit Card'),
(2, 2, '2023-02-21 14:15:00', 1, 'Completed', 'PayPal'),
(3, 3, '2023-03-11 09:45:00', 1, 'Completed', 'Credit Card'),
(4, 4, '2023-04-06 16:20:00', 1, 'Completed', 'Debit Card'),
(5, 5, '2023-05-13 11:00:00', 1, 'Completed', 'Credit Card'),
(6, 6, '2023-06-19 13:30:00', 1, 'Completed', 'PayPal'),
(7, 7, '2023-07-23 10:00:00', 1, 'Completed', 'Credit Card'),
(8, 8, '2023-08-31 15:45:00', 1, 'Completed', 'Debit Card'),
(9, 9, '2023-09-15 09:00:00', 1, 'Completed', 'Credit Card'),
(10, 10, '2023-10-02 12:00:00', 2, 'Completed', 'PayPal');

-- Insert Order Items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, discount_pct, item_price) VALUES
(1, 1, 1, 1, 5.00, 999.99),
(2, 1, 3, 2, 0.00, 399.99),
(3, 2, 5, 3, 10.00, 69.99),
(4, 2, 6, 1, 0.00, 199.99),
(5, 3, 8, 1, 15.00, 449.99),
(6, 4, 2, 2, 5.00, 899.99),
(7, 5, 4, 1, 0.00, 499.99),
(8, 5, 7, 1, 10.00, 249.99),
(9, 6, 9, 3, 0.00, 129.99),
(10, 7, 1, 1, 0.00, 999.99),
(11, 7, 2, 1, 5.00, 899.99),
(12, 8, 6, 2, 0.00, 199.99),
(13, 9, 8, 1, 0.00, 449.99),
(14, 9, 9, 2, 10.00, 129.99),
(15, 10, 10, 3, 0.00, 19.99);

-- Insert Returns
INSERT INTO returns (return_id, order_item_id, return_date, return_reason, refund_amount) VALUES
(1, 2, '2023-01-20', 'Defective product', 799.98),
(2, 4, '2023-02-25', 'Wrong size', 199.99),
(3, 6, '2023-04-10', 'Not as described', 1799.98),
(4, 8, '2023-05-15', 'Damaged during shipping', 249.99),
(5, 11, '2023-07-25', 'Changed mind', 899.99),
(6, 13, '2023-09-20', 'Defective product', 449.99),
(7, 15, '2023-10-05', 'Wrong item', 59.97);