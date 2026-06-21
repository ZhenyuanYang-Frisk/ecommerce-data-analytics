import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# ==================== Database Configuration ====================
try:
    from config import DB_CONFIG
except ImportError:
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'your_password',
        'database': 'your_database',
        'charset': 'utf8mb4'
    }
    print("⚠️  config.py not found. Using default configuration.")


# ==================== Database Connection Function ====================
def query_data(sql):
    conn = None
    try:
        if not sql or not sql.strip():
            raise ValueError("SQL query cannot be empty")

        conn = pymysql.connect(**DB_CONFIG)
        print(f"📝 Executing SQL: {sql[:200]}{'...' if len(sql) > 200 else ''}")
        df = pd.read_sql(sql, conn)
        print(f"📊 Returned {len(df)} rows")
        return df

    except pymysql.err.OperationalError as e:
        error_msg = f"Database connection failed: {e}\n\nPlease check:\n1. MySQL service is running\n2. Host/port are correct\n3. Username/password are correct"
        print(f"❌ {error_msg}")
        messagebox.showerror("Connection Error", error_msg)
        return None

    except pymysql.err.ProgrammingError as e:
        error_msg = f"SQL syntax error: {e}\n\nPlease check your SQL query."
        print(f"❌ {error_msg}")
        messagebox.showerror("SQL Error", error_msg)
        return None

    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Unexpected Error", error_msg)
        return None

    finally:
        if conn:
            try:
                conn.close()
                print("🔒 Database connection closed")
            except Exception as e:
                print(f"⚠️  Error closing connection: {e}")


# ==================== Chart Display Functions ====================
def show_sales_chart():
    """Display daily sales trend chart using order_items table"""
    try:
        sql = """
            SELECT 
                DATE(o.order_date) as order_date,
                COUNT(DISTINCT o.order_id) as order_count,
                ROUND(SUM(oi.quantity * oi.item_price * (1 - oi.discount_pct / 100)), 2) as total_sales
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY DATE(o.order_date)
            ORDER BY order_date DESC
            LIMIT 30
        """
        df = query_data(sql)
        if df is None or df.empty:
            messagebox.showinfo("Info", "No sales data available for chart")
            return

        # Reverse to show chronological order
        df = df.sort_values('order_date')

        chart_window = tk.Toplevel()
        chart_window.title("📊 Daily Sales Trend (Last 30 Days)")
        chart_window.geometry("900x600")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Sales trend
        ax1.plot(df['order_date'], df['total_sales'], marker='o', linestyle='-',
                 color='#2E86AB', linewidth=2, markersize=6)
        ax1.set_title('Daily Sales Revenue', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Total Sales ($)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # Order count trend
        ax2.bar(df['order_date'], df['order_count'], color='#A23B72', alpha=0.7)
        ax2.set_title('Daily Order Count', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Number of Orders')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Info label
        info_label = tk.Label(chart_window,
                              text=f"📊 Showing last 30 days | Total revenue: ${df['total_sales'].sum():.2f} | Total orders: {df['order_count'].sum()}",
                              font=('Arial', 10), fg='gray')
        info_label.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Chart Error", f"Failed to generate sales chart: {e}")


def show_return_chart():
    """Display daily return trend chart"""
    try:
        sql = """
            SELECT 
                return_date,
                COUNT(*) as return_count,
                ROUND(SUM(refund_amount), 2) as total_refund
            FROM returns
            GROUP BY return_date
            ORDER BY return_date DESC
            LIMIT 30
        """
        df = query_data(sql)
        if df is None or df.empty:
            messagebox.showinfo("Info", "No return data available for chart")
            return

        # Reverse to show chronological order
        df = df.sort_values('return_date')

        chart_window = tk.Toplevel()
        chart_window.title("📊 Daily Return Trend (Last 30 Days)")
        chart_window.geometry("900x600")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Refund amount trend
        ax1.plot(df['return_date'], df['total_refund'], marker='s', linestyle='-',
                 color='#D64933', linewidth=2, markersize=6)
        ax1.set_title('Daily Refund Amount', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Total Refund ($)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # Return count trend
        ax2.bar(df['return_date'], df['return_count'], color='#F18F01', alpha=0.7)
        ax2.set_title('Daily Return Count', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Number of Returns')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Info label
        info_label = tk.Label(chart_window,
                              text=f"📊 Showing last 30 days | Total refund: ${df['total_refund'].sum():.2f} | Total returns: {df['return_count'].sum()}",
                              font=('Arial', 10), fg='gray')
        info_label.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Chart Error", f"Failed to generate return chart: {e}")


# ==================== Table Display Window ====================
def show_table_window(df, title="Data Preview", sortable=True):
    if df is None:
        messagebox.showwarning("Warning", "No data to display")
        return

    if df.empty:
        messagebox.showwarning("Warning", "No data to display (empty result set)")
        return

    try:
        window = tk.Toplevel()
        window.title(title)
        window.geometry("1100x650")

        toolbar = tk.Frame(window)
        toolbar.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(toolbar, text=f"Total {len(df)} rows × {len(df.columns)} columns",
                 font=('Arial', 12)).pack(side=tk.LEFT)

        if sortable and len(df) > 0:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                tk.Label(toolbar, text="  |  Sort by:", font=('Arial', 11)).pack(side=tk.LEFT, padx=(20, 5))

                sort_var = tk.StringVar(value="No Sort")
                sort_combo = ttk.Combobox(toolbar, textvariable=sort_var,
                                          values=["No Sort"] + numeric_cols,
                                          width=15, state="readonly")
                sort_combo.pack(side=tk.LEFT, padx=5)

                tk.Label(toolbar, text="Order:", font=('Arial', 11)).pack(side=tk.LEFT, padx=5)
                order_var = tk.StringVar(value="Descending")
                order_combo = ttk.Combobox(toolbar, textvariable=order_var,
                                           values=["Ascending", "Descending"],
                                           width=8, state="readonly")
                order_combo.pack(side=tk.LEFT, padx=5)

                def apply_sort():
                    try:
                        col = sort_var.get()
                        if col == "No Sort" or col not in df.columns:
                            return
                        ascending = (order_var.get() == "Ascending")
                        sorted_df = df.sort_values(by=col, ascending=ascending)
                        refresh_table(tree, sorted_df)
                    except Exception as e:
                        messagebox.showerror("Sort Error", f"Failed to sort: {e}")

                tk.Button(toolbar, text="🔄 Apply Sort", command=apply_sort,
                          font=('Arial', 10), bg='#e8f0fe').pack(side=tk.LEFT, padx=10)

        def export_csv():
            try:
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                if file_path:
                    df.to_csv(file_path, index=False, encoding='utf-8-sig')
                    messagebox.showinfo("Success", f"Exported to: {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")

        tk.Button(toolbar, text="📥 Export CSV", command=export_csv).pack(side=tk.RIGHT, padx=5)

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tree = ttk.Treeview(frame)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=tree.xview)
        h_scrollbar.pack(fill=tk.X, padx=10)
        tree.configure(xscrollcommand=h_scrollbar.set)

        def refresh_table(tree_widget, data_df):
            try:
                for item in tree_widget.get_children():
                    tree_widget.delete(item)

                columns = list(data_df.columns)
                tree_widget['columns'] = columns
                tree_widget['show'] = 'headings'

                for col in columns:
                    tree_widget.heading(col, text=col)
                    if data_df[col].dtype in ['int64', 'float64']:
                        max_len = max(len(str(col)),
                                      data_df[col].astype(str).str.len().max() if len(data_df) > 0 else 0)
                        tree_widget.column(col, width=min(max(100, max_len * 10), 250), anchor='e')
                    else:
                        max_len = max(len(str(col)),
                                      data_df[col].astype(str).str.len().max() if len(data_df) > 0 else 0)
                        tree_widget.column(col, width=min(max(100, max_len * 10), 300), anchor='center')

                for idx, row in data_df.iterrows():
                    values = []
                    for v in row:
                        if pd.isna(v):
                            values.append('')
                        else:
                            values.append(str(v))
                    tree_widget.insert('', 'end', values=values)
            except Exception as e:
                messagebox.showerror("Display Error", f"Failed to refresh table: {e}")

        refresh_table(tree, df)

    except Exception as e:
        messagebox.showerror("Window Error", f"Failed to create display window: {e}")


# ==================== Search Customer Window ====================
def search_customer_window():
    try:
        search_win = tk.Toplevel()
        search_win.title("🔍 Search Customers")
        search_win.geometry("500x300")
        search_win.resizable(False, False)

        tk.Label(search_win, text="🔍 Customer Search", font=('Arial', 18, 'bold')).pack(pady=20)

        search_frame = tk.Frame(search_win)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Enter Name (First or Last):", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=25, font=('Arial', 12))
        search_entry.pack(side=tk.LEFT, padx=5)

        def do_search():
            try:
                keyword = search_var.get().strip()
                if not keyword:
                    messagebox.showwarning("Warning", "Please enter a name to search")
                    return

                sql = f"""
                    SELECT customer_id, first_name, last_name, email, 
                           signup_date, customer_type, acquisition_channel,
                           city, province, country, region_id
                    FROM customers 
                    WHERE first_name LIKE '%{keyword}%' 
                       OR last_name LIKE '%{keyword}%'
                    ORDER BY customer_id
                """
                df = query_data(sql)
                if df is not None and not df.empty:
                    show_table_window(df, f"Search: {keyword}", sortable=True)
                else:
                    messagebox.showinfo("Info", f"No customers found containing '{keyword}'")
            except Exception as e:
                messagebox.showerror("Search Error", f"Search failed: {e}")

        def do_exact_search():
            try:
                keyword = search_var.get().strip()
                if not keyword:
                    messagebox.showwarning("Warning", "Please enter a name to search")
                    return

                sql = f"""
                    SELECT customer_id, first_name, last_name, email, 
                           signup_date, customer_type, acquisition_channel,
                           city, province, country, region_id
                    FROM customers 
                    WHERE first_name LIKE '{keyword}' 
                       OR last_name LIKE '{keyword}'
                       OR CONCAT(first_name, ' ', last_name) LIKE '{keyword}'
                    ORDER BY customer_id
                """
                df = query_data(sql)
                if df is not None and not df.empty:
                    show_table_window(df, f"Exact Search: {keyword}", sortable=True)
                else:
                    messagebox.showinfo("Info", f"No customer named '{keyword}' found")
            except Exception as e:
                messagebox.showerror("Search Error", f"Search failed: {e}")

        tk.Button(search_frame, text="🔍 Fuzzy Search", command=do_search,
                  font=('Arial', 11), bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="🎯 Exact Search", command=do_exact_search,
                  font=('Arial', 11), bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=5)

        tk.Label(search_win, text="💡 Fuzzy Search: Enter partial name",
                 font=('Arial', 10), fg='gray').pack(pady=10)
        tk.Label(search_win, text="💡 Exact Search: Enter full name",
                 font=('Arial', 10), fg='gray').pack(pady=5)

        search_entry.bind('<Return>', lambda e: do_search())

        tk.Button(search_win, text="Close", command=search_win.destroy,
                  width=15, height=1, font=('Arial', 11)).pack(pady=15)

    except Exception as e:
        messagebox.showerror("Window Error", f"Failed to open search window: {e}")


# ==================== Order Detail Query Window ====================
def show_order_detail_window():
    try:
        detail_win = tk.Toplevel()
        detail_win.title("🔍 Order Detail Query")
        detail_win.geometry("600x450")
        detail_win.resizable(False, False)

        tk.Label(detail_win, text="🔍 Order Detail Query", font=('Arial', 18, 'bold')).pack(pady=20)
        tk.Label(detail_win, text="Enter Order ID to view products and price details",
                 font=('Arial', 12)).pack(pady=5)

        tk.Frame(detail_win, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

        input_frame = tk.Frame(detail_win)
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Order ID:", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=10)

        order_id_var = tk.StringVar()
        order_id_entry = tk.Entry(input_frame, textvariable=order_id_var, width=20, font=('Arial', 14))
        order_id_entry.pack(side=tk.LEFT, padx=10)

        def do_query_order_detail():
            try:
                order_id = order_id_var.get().strip()
                if not order_id:
                    messagebox.showwarning("Warning", "Please enter an Order ID")
                    return

                check_sql = f"SELECT COUNT(*) as cnt FROM orders WHERE order_id = {order_id}"
                check_df = query_data(check_sql)
                if check_df is None or check_df.empty or check_df.iloc[0]['cnt'] == 0:
                    messagebox.showwarning("Warning", f"Order ID '{order_id}' does not exist")
                    return

                sql = f"""
                    SELECT 
                        oi.order_item_id,
                        oi.product_id,
                        p.product_name,
                        oi.quantity,
                        oi.item_price as unit_price,
                        oi.discount_pct as discount_pct,
                        ROUND(oi.quantity * oi.item_price, 2) as subtotal,
                        ROUND(oi.quantity * oi.item_price * (oi.discount_pct / 100), 2) as discount_amount,
                        ROUND(oi.quantity * oi.item_price * (1 - oi.discount_pct / 100), 2) as total_paid
                    FROM order_items oi
                    LEFT JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = {order_id}
                    ORDER BY oi.order_item_id
                """
                df = query_data(sql)

                if df is None or df.empty:
                    messagebox.showinfo("Info", f"Order {order_id} has no items")
                    return

                total_original = df['subtotal'].sum()
                total_discount = df['discount_amount'].sum()
                total_paid = df['total_paid'].sum()
                total_quantity = df['quantity'].sum()

                title = f"Order {order_id} Detail  |  Total Qty: {total_quantity}  |  Subtotal: ${total_original:.2f}  |  Discount: ${total_discount:.2f}  |  Total: ${total_paid:.2f}"

                show_table_window(df, title, sortable=True)

            except Exception as e:
                messagebox.showerror("Query Error", f"Failed to query order detail: {e}")

        btn_frame = tk.Frame(detail_win)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔍 Query Order Detail", command=do_query_order_detail,
                  width=20, height=2, font=('Arial', 12), bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=10)

        order_id_entry.bind('<Return>', lambda e: do_query_order_detail())

        tk.Frame(detail_win, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

        info_frame = tk.Frame(detail_win)
        info_frame.pack(pady=10)

        tk.Label(info_frame, text="💡 Sample Order IDs:", font=('Arial', 11)).pack(side=tk.LEFT, padx=5)

        try:
            conn = pymysql.connect(**DB_CONFIG)
            sample_df = pd.read_sql("SELECT order_id FROM orders LIMIT 5", conn)
            conn.close()
            if not sample_df.empty:
                sample_ids = ', '.join([str(x) for x in sample_df['order_id'].tolist()])
                tk.Label(info_frame, text=sample_ids, font=('Arial', 11, 'bold'), fg='blue').pack(side=tk.LEFT, padx=5)
            else:
                tk.Label(info_frame, text="(No orders found)", font=('Arial', 11), fg='gray').pack(side=tk.LEFT, padx=5)
        except Exception:
            tk.Label(info_frame, text="(Unable to load samples)", font=('Arial', 11), fg='gray').pack(side=tk.LEFT,
                                                                                                      padx=5)

        tk.Label(detail_win, text="💡 Results include: Product Name, Qty, Unit Price, Subtotal, Discount, Total Paid",
                 font=('Arial', 10), fg='gray').pack(pady=5)
        tk.Label(detail_win, text="💡 Summary shows: Total Qty, Subtotal, Discount, Total",
                 font=('Arial', 10), fg='gray').pack(pady=2)

        tk.Button(detail_win, text="Close", command=detail_win.destroy,
                  width=15, height=1, font=('Arial', 11)).pack(pady=15)

    except Exception as e:
        messagebox.showerror("Window Error", f"Failed to open order detail window: {e}")


# ==================== Test Database Connection ====================
def test_database_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("✅ Database connection test: SUCCESS")
                conn.close()
                return True
        conn.close()
        return False
    except Exception as e:
        print(f"❌ Database connection test: FAILED - {e}")
        return False


# ==================== Main Application Class ====================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 E-Commerce Data Analytics Platform")
        self.root.geometry("580x780")
        self.root.resizable(False, False)
        self.current_frame = None

        if not test_database_connection():
            if not messagebox.askyesno("Database Warning",
                                       "Cannot connect to database. Some features may not work.\n\n"
                                       "Please check your config.py settings.\n\n"
                                       "Do you want to continue anyway?"):
                sys.exit(1)

        self.show_main_page()

    def clear_frame(self):
        if self.current_frame:
            try:
                self.current_frame.destroy()
            except Exception as e:
                print(f"⚠️  Error clearing frame: {e}")

    def show_main_page(self):
        try:
            self.clear_frame()
            self.current_frame = tk.Frame(self.root)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.current_frame, text="🛒 E-Commerce Data Analytics Platform",
                     font=('Arial', 22, 'bold')).pack(pady=25)
            tk.Label(self.current_frame, text="Select a data module to analyze",
                     font=('Arial', 14)).pack(pady=5)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            btn_kwargs = {'width': 35, 'height': 2, 'font': ('Arial', 13)}

            tk.Button(self.current_frame, text="📦 Order Analysis",
                      command=lambda: self.show_orders_page(),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📋 Product Analysis",
                      command=lambda: self.show_products_page(),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="🔄 Return Analysis",
                      command=lambda: self.show_returns_page(),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📂 Category Analysis",
                      command=lambda: self.show_categories_page(),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="👤 Customer Analysis",
                      command=lambda: self.show_customers_page(),
                      **btn_kwargs).pack(pady=6)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            # Chart buttons on main page
            chart_frame = tk.Frame(self.current_frame)
            chart_frame.pack(pady=5)

            tk.Button(chart_frame, text="📊 Sales Chart", command=show_sales_chart,
                      width=20, height=1, font=('Arial', 11), bg='#2E86AB', fg='white').pack(side=tk.LEFT, padx=5)

            tk.Button(chart_frame, text="📊 Return Chart", command=show_return_chart,
                      width=20, height=1, font=('Arial', 11), bg='#D64933', fg='white').pack(side=tk.LEFT, padx=5)

            tk.Label(self.current_frame, text="💡 Click a button to enter the corresponding module",
                     font=('Arial', 10), fg='gray').pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load main page: {e}")

    # ==================== Orders Page ====================
    def show_orders_page(self):
        try:
            self.clear_frame()
            self.current_frame = tk.Frame(self.root)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.current_frame, text="📦 Order Analysis",
                     font=('Arial', 20, 'bold')).pack(pady=10)
            tk.Label(self.current_frame, text="Select filters and click Query",
                     font=('Arial', 12)).pack(pady=2)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=30, pady=8)

            # Chart buttons for orders
            chart_btn_frame = tk.Frame(self.current_frame)
            chart_btn_frame.pack(pady=3)

            tk.Button(chart_btn_frame, text="📊 Show Sales Chart", command=show_sales_chart,
                      width=20, height=1, font=('Arial', 10), bg='#2E86AB', fg='white').pack(side=tk.LEFT, padx=5)

            # Order Detail Query Button
            detail_btn_frame = tk.Frame(self.current_frame)
            detail_btn_frame.pack(pady=5)

            tk.Button(detail_btn_frame,
                      text="🔍 Query Order Detail (by Order ID)",
                      command=show_order_detail_window,
                      width=30, height=2, font=('Arial', 11),
                      bg='#2196F3', fg='white').pack()

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=30, pady=8)

            # Filter Section
            filter_frame = tk.Frame(self.current_frame)
            filter_frame.pack(pady=5, padx=10)

            def get_filter_values():
                values = {'status': [], 'method': [], 'region': []}
                try:
                    conn = pymysql.connect(**DB_CONFIG)
                    status_df = pd.read_sql("SELECT DISTINCT order_status FROM orders WHERE order_status IS NOT NULL",
                                            conn)
                    values['status'] = sorted(status_df['order_status'].tolist()) if not status_df.empty else []

                    method_df = pd.read_sql(
                        "SELECT DISTINCT payment_method FROM orders WHERE payment_method IS NOT NULL", conn)
                    values['method'] = sorted(method_df['payment_method'].tolist()) if not method_df.empty else []

                    region_df = pd.read_sql("SELECT DISTINCT region_id FROM orders WHERE region_id IS NOT NULL", conn)
                    values['region'] = sorted(region_df['region_id'].tolist()) if not region_df.empty else []

                    conn.close()
                except Exception as e:
                    print(f"Failed to get filter values: {e}")
                return values

            filter_values = get_filter_values()

            # Row 1: Date Range
            date_frame = tk.Frame(filter_frame)
            date_frame.pack(pady=4)

            tk.Label(date_frame, text="📅 Date:", font=('Arial', 11)).pack(side=tk.LEFT, padx=2)

            tk.Label(date_frame, text="From:", font=('Arial', 10)).pack(side=tk.LEFT, padx=2)
            start_date_var = tk.StringVar()
            tk.Entry(date_frame, textvariable=start_date_var, width=10, font=('Arial', 10)).pack(side=tk.LEFT, padx=1)
            tk.Label(date_frame, text="(YYYY-MM-DD)", font=('Arial', 7), fg='gray').pack(side=tk.LEFT)

            tk.Label(date_frame, text="To:", font=('Arial', 10)).pack(side=tk.LEFT, padx=2)
            end_date_var = tk.StringVar()
            tk.Entry(date_frame, textvariable=end_date_var, width=10, font=('Arial', 10)).pack(side=tk.LEFT, padx=1)
            tk.Label(date_frame, text="(YYYY-MM-DD)", font=('Arial', 7), fg='gray').pack(side=tk.LEFT)

            # Row 2: Status + Payment
            filter_row1 = tk.Frame(filter_frame)
            filter_row1.pack(pady=3)

            tk.Label(filter_row1, text="📌 Status:", font=('Arial', 11)).pack(side=tk.LEFT, padx=2)
            status_var = tk.StringVar(value="All")
            status_combo = ttk.Combobox(filter_row1, textvariable=status_var,
                                        values=["All"] + filter_values['status'],
                                        width=12, state="readonly")
            status_combo.pack(side=tk.LEFT, padx=2)

            tk.Label(filter_row1, text="  💳 Payment:", font=('Arial', 11)).pack(side=tk.LEFT, padx=2)
            method_var = tk.StringVar(value="All")
            method_combo = ttk.Combobox(filter_row1, textvariable=method_var,
                                        values=["All"] + filter_values['method'],
                                        width=12, state="readonly")
            method_combo.pack(side=tk.LEFT, padx=2)

            # Row 3: Region + Sort
            filter_row2 = tk.Frame(filter_frame)
            filter_row2.pack(pady=3)

            tk.Label(filter_row2, text="🌍 Region:", font=('Arial', 11)).pack(side=tk.LEFT, padx=2)
            region_var = tk.StringVar(value="All")
            region_combo = ttk.Combobox(filter_row2, textvariable=region_var,
                                        values=["All"] + filter_values['region'],
                                        width=8, state="readonly")
            region_combo.pack(side=tk.LEFT, padx=2)

            tk.Label(filter_row2, text="  Sort:", font=('Arial', 11)).pack(side=tk.LEFT, padx=2)
            order_var = tk.StringVar(value="Date Desc (Newest)")
            order_combo = ttk.Combobox(filter_row2, textvariable=order_var,
                                       values=[
                                           "Date Desc (Newest)",
                                           "Date Asc (Oldest)",
                                           "ID Desc (Largest)",
                                           "ID Asc (Smallest)"
                                       ],
                                       width=15, state="readonly")
            order_combo.pack(side=tk.LEFT, padx=2)

            # Row 4: Buttons
            btn_frame = tk.Frame(filter_frame)
            btn_frame.pack(pady=6)

            def do_query():
                try:
                    sql = "SELECT order_id, customer_id, order_date, region_id, order_status, payment_method FROM orders WHERE 1=1"

                    start_date = start_date_var.get().strip()
                    end_date = end_date_var.get().strip()
                    if start_date:
                        sql += f" AND order_date >= '{start_date}'"
                    if end_date:
                        sql += f" AND order_date <= '{end_date}'"

                    status = status_var.get()
                    if status != "All":
                        sql += f" AND order_status = '{status}'"

                    method = method_var.get()
                    if method != "All":
                        sql += f" AND payment_method = '{method}'"

                    region = region_var.get()
                    if region != "All":
                        sql += f" AND region_id = {region}"

                    order = order_var.get()
                    if order == "Date Desc (Newest)":
                        sql += " ORDER BY order_date DESC"
                    elif order == "Date Asc (Oldest)":
                        sql += " ORDER BY order_date"
                    elif order == "ID Desc (Largest)":
                        sql += " ORDER BY order_id DESC"
                    else:
                        sql += " ORDER BY order_id"

                    df = query_data(sql)
                    show_table_window(df, "Order Query Results", sortable=True)
                except Exception as e:
                    messagebox.showerror("Query Error", f"Query failed: {e}")

            tk.Button(btn_frame, text="🔍 Query", command=do_query,
                      width=12, height=1, font=('Arial', 11),
                      bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=4)

            def reset_filters():
                try:
                    start_date_var.set("")
                    end_date_var.set("")
                    status_var.set("All")
                    method_var.set("All")
                    region_var.set("All")
                    order_var.set("Date Desc (Newest)")
                except Exception as e:
                    print(f"Reset error: {e}")

            tk.Button(btn_frame, text="🔄 Reset", command=reset_filters,
                      width=8, height=1, font=('Arial', 11),
                      bg='#f0f0f0').pack(side=tk.LEFT, padx=4)

            def view_all():
                try:
                    df = query_data(
                        "SELECT order_id, customer_id, order_date, region_id, order_status, payment_method FROM orders ORDER BY order_date DESC")
                    show_table_window(df, "All Orders", sortable=True)
                except Exception as e:
                    messagebox.showerror("Query Error", f"Failed to load all orders: {e}")

            tk.Button(btn_frame, text="📋 View All", command=view_all,
                      width=10, height=1, font=('Arial', 11),
                      bg='#e8f0fe').pack(side=tk.LEFT, padx=4)

            def show_stats():
                try:
                    sql = """
                        SELECT 
                            COUNT(*) as total_orders,
                            COUNT(DISTINCT customer_id) as total_customers,
                            COUNT(DISTINCT region_id) as total_regions
                        FROM orders
                    """
                    df = query_data(sql)
                    show_table_window(df, "Order Statistics", sortable=False)
                except Exception as e:
                    messagebox.showerror("Stats Error", f"Failed to load statistics: {e}")

            tk.Button(btn_frame, text="📊 Stats", command=show_stats,
                      width=8, height=1, font=('Arial', 11),
                      bg='#fff3e0').pack(side=tk.LEFT, padx=4)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=30, pady=8)

            tk.Button(self.current_frame, text="⬅ Back to Main Menu",
                      command=self.show_main_page,
                      width=22, height=1, font=('Arial', 12),
                      bg='#f0f0f0').pack(pady=8)

            tk.Label(self.current_frame, text="💡 Combine multiple filters for precise results",
                     font=('Arial', 9), fg='gray').pack(pady=2)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders page: {e}")

    # ==================== Products Page ====================
    def show_products_page(self):
        try:
            self.clear_frame()
            self.current_frame = tk.Frame(self.root)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.current_frame, text="📋 Product Analysis",
                     font=('Arial', 20, 'bold')).pack(pady=20)
            tk.Label(self.current_frame, text="Select a product analysis dimension",
                     font=('Arial', 12)).pack(pady=5)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            def make_query(sql, title):
                def inner():
                    try:
                        df = query_data(sql)
                        show_table_window(df, title, sortable=True)
                    except Exception as e:
                        messagebox.showerror("Query Error", f"Failed to load data: {e}")

                return inner

            btn_kwargs = {'width': 35, 'height': 2, 'font': ('Arial', 12)}

            tk.Button(self.current_frame, text="📋 View All Products",
                      command=make_query("""
                          SELECT product_id, product_name, category_id, 
                                 unit_cost, unit_price, launch_date, active_flag
                          FROM products 
                          ORDER BY product_id
                      """, "All Products"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📅 Sort by Launch Date (Newest)",
                      command=make_query("""
                          SELECT product_id, product_name, category_id, 
                                 unit_cost, unit_price, launch_date, active_flag
                          FROM products 
                          ORDER BY launch_date DESC
                      """, "Launch Date (Newest)"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📅 Sort by Launch Date (Oldest)",
                      command=make_query("""
                          SELECT product_id, product_name, category_id, 
                                 unit_cost, unit_price, launch_date, active_flag
                          FROM products 
                          ORDER BY launch_date
                      """, "Launch Date (Oldest)"),
                      **btn_kwargs).pack(pady=6)

            tk.Frame(self.current_frame, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=60, pady=5)

            flag_frame = tk.Frame(self.current_frame)
            flag_frame.pack(pady=8)

            tk.Label(flag_frame, text="🔍 Search by active_flag:", font=('Arial', 11)).pack(side=tk.LEFT, padx=5)

            flag_var = tk.StringVar()
            flag_entry = tk.Entry(flag_frame, textvariable=flag_var, width=20, font=('Arial', 11))
            flag_entry.pack(side=tk.LEFT, padx=5)

            def search_by_flag():
                try:
                    flag = flag_var.get().strip()
                    if not flag:
                        messagebox.showwarning("Warning", "Please enter an active_flag value")
                        return

                    sql = f"""
                        SELECT product_id, product_name, category_id, 
                               unit_cost, unit_price, launch_date, active_flag
                        FROM products 
                        WHERE active_flag LIKE '%{flag}%'
                        ORDER BY product_id
                    """
                    df = query_data(sql)
                    if df is not None and not df.empty:
                        show_table_window(df, f"Search active_flag: {flag}", sortable=True)
                    else:
                        messagebox.showinfo("Info", f"No products found with active_flag containing '{flag}'")
                except Exception as e:
                    messagebox.showerror("Search Error", f"Search failed: {e}")

            flag_entry.bind('<Return>', lambda e: search_by_flag())

            tk.Button(flag_frame, text="🔍 Search", command=search_by_flag,
                      width=10, height=1, font=('Arial', 11), bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=5)

            def clear_flag_search():
                flag_var.set("")

            tk.Button(flag_frame, text="Clear", command=clear_flag_search,
                      width=6, height=1, font=('Arial', 11), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            tk.Button(self.current_frame, text="⬅ Back to Main Menu",
                      command=self.show_main_page,
                      width=20, height=1, font=('Arial', 12), bg='#f0f0f0').pack(pady=10)

            tk.Label(self.current_frame, text="💡 Sort by any column in the table popup",
                     font=('Arial', 9), fg='gray').pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products page: {e}")

    # ==================== Returns Page ====================
    def show_returns_page(self):
        try:
            self.clear_frame()
            self.current_frame = tk.Frame(self.root)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.current_frame, text="🔄 Return Analysis",
                     font=('Arial', 20, 'bold')).pack(pady=20)
            tk.Label(self.current_frame, text="Select a return analysis dimension",
                     font=('Arial', 12)).pack(pady=5)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            # Chart button for returns
            chart_btn_frame = tk.Frame(self.current_frame)
            chart_btn_frame.pack(pady=5)

            tk.Button(chart_btn_frame, text="📊 Show Return Chart", command=show_return_chart,
                      width=20, height=1, font=('Arial', 10), bg='#D64933', fg='white').pack(side=tk.LEFT, padx=5)

            tk.Frame(self.current_frame, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=60, pady=5)

            def make_query(sql, title):
                def inner():
                    try:
                        df = query_data(sql)
                        show_table_window(df, title, sortable=True)
                    except Exception as e:
                        messagebox.showerror("Query Error", f"Failed to load data: {e}")

                return inner

            btn_kwargs = {'width': 35, 'height': 2, 'font': ('Arial', 12)}

            tk.Button(self.current_frame, text="📋 View All Returns",
                      command=make_query("""
                          SELECT return_id, order_item_id, return_date, 
                                 return_reason, refund_amount 
                          FROM returns 
                          ORDER BY return_id
                      """, "All Returns"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📅 Sort by Date (Newest)",
                      command=make_query("""
                          SELECT return_id, order_item_id, return_date, 
                                 return_reason, refund_amount 
                          FROM returns 
                          ORDER BY return_date DESC
                      """, "Sort by Date"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="💰 Sort by Amount (Highest)",
                      command=make_query("""
                          SELECT return_id, order_item_id, return_date, 
                                 return_reason, refund_amount 
                          FROM returns 
                          ORDER BY CAST(refund_amount AS DECIMAL(10,2)) DESC
                      """, "Sort by Amount"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📊 Return Reason Statistics",
                      command=make_query("""
                          SELECT return_reason, COUNT(*) as count 
                          FROM returns 
                          WHERE return_reason IS NOT NULL 
                          GROUP BY return_reason 
                          ORDER BY count DESC
                      """, "Return Reason Stats"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="📈 Daily Return Trend",
                      command=make_query("""
                          SELECT DATE(return_date) as return_date, 
                                 COUNT(*) as return_count,
                                 ROUND(SUM(refund_amount), 2) as total_refund
                          FROM returns 
                          GROUP BY DATE(return_date)
                          ORDER BY return_date DESC
                      """, "Daily Return Trend"),
                      **btn_kwargs).pack(pady=6)

            tk.Button(self.current_frame, text="💰 Refund Amount Statistics",
                      command=make_query("""
                          SELECT 
                              COUNT(*) as return_count,
                              ROUND(SUM(refund_amount), 2) as total_refund,
                              ROUND(AVG(refund_amount), 2) as avg_refund,
                              ROUND(MAX(refund_amount), 2) as max_refund,
                              ROUND(MIN(refund_amount), 2) as min_refund
                          FROM returns
                      """, "Refund Statistics"),
                      **btn_kwargs).pack(pady=6)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            tk.Button(self.current_frame, text="⬅ Back to Main Menu",
                      command=self.show_main_page,
                      width=20, height=1, font=('Arial', 12), bg='#f0f0f0').pack(pady=10)

            tk.Label(self.current_frame, text="💡 Sort by any column in the table popup",
                     font=('Arial', 9), fg='gray').pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load returns page: {e}")

    # ==================== Categories Page ====================
    def show_categories_page(self):
        try:
            self.clear_frame()
            self.current_frame = tk.Frame(self.root)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.current_frame, text="📂 Category Analysis",
                     font=('Arial', 20, 'bold')).pack(pady=20)
            tk.Label(self.current_frame, text="Click a category to view its products",
                     font=('Arial', 12)).pack(pady=5)

            tk.Frame(self.current_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            canvas = tk.Canvas(self.current_frame)
            scrollbar = tk.Scrollbar(self.current_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
            canvas.configure(yscrollcommand=scrollbar.set)

            def on_canvas_configure(event):
                canvas.itemconfig(1, width=event.width)
                canvas.configure(scrollregion=canvas.bbox("all"))

            canvas.bind("<Configure>", on_canvas_configure)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            content_frame = tk.Frame(scrollable_frame)
            content_frame.pack(expand=True)

            def get_categories():
                try:
                    conn = pymysql.connect(**DB_CONFIG)
                    df = pd.read_sql("SELECT category_id, category_name FROM categories ORDER BY category_id", conn)
                    conn.close()
                    return df
                except Exception as e:
                    print(f"Failed to get categories: {e}")
                    messagebox.showwarning("Warning", f"Could not load categories: {e}")
                    return pd.DataFrame()

            def show_products_by_category(category_id, category_name):
                try:
                    sql = f"""
                        SELECT product_id, product_name, unit_cost, unit_price, 
                               launch_date, active_flag
                        FROM products 
                        WHERE category_id = {category_id}
                        ORDER BY product_id
                    """
                    df = query_data(sql)
                    if df is not None and not df.empty:
                        show_table_window(df, f"📂 {category_name} Products", sortable=True)
                    else:
                        messagebox.showinfo("Info", f"No products in category '{category_name}'")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load products: {e}")

            categories_df = get_categories()

            btn_kwargs = {'width': 30, 'height': 2, 'font': ('Arial', 12)}

            if categories_df.empty:
                tk.Label(content_frame, text="⚠️ No categories found", font=('Arial', 14), fg='red').pack(pady=30)
            else:
                for _, row in categories_df.iterrows():
                    cat_id = row['category_id']
                    cat_name = row['category_name']
                    btn_text = f"📂 {cat_name} (ID: {cat_id})"
                    tk.Button(content_frame, text=btn_text,
                              command=lambda cid=cat_id, cname=cat_name: show_products_by_category(cid, cname),
                              **btn_kwargs).pack(pady=4)

            tk.Frame(content_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            def view_all_products():
                try:
                    df = query_data("""
                        SELECT product_id, product_name, category_id, 
                               unit_cost, unit_price, launch_date, active_flag
                        FROM products 
                        ORDER BY product_id
                    """)
                    show_table_window(df, "All Products", sortable=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load products: {e}")

            tk.Button(content_frame, text="📋 View All Products", command=view_all_products,
                      width=30, height=1, font=('Arial', 12), bg='#e8f0fe').pack(pady=5)

            tk.Button(content_frame, text="⬅ Back to Main Menu",
                      command=self.show_main_page,
                      width=20, height=1, font=('Arial', 12), bg='#f0f0f0').pack(pady=10)

            tk.Label(content_frame, text="💡 Click a category to view its products",
                     font=('Arial', 9), fg='gray').pack(pady=5)

            tk.Label(content_frame, text="", font=('Arial', 8)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories page: {e}")

    # ==================== Customers Page ====================
    def show_customers_page(self):
        try:
            self.clear_frame()
            self.current_frame = tk.Frame(self.root)
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(self.current_frame)
            scrollbar = tk.Scrollbar(self.current_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
            canvas.configure(yscrollcommand=scrollbar.set)

            def on_canvas_configure(event):
                canvas.itemconfig(1, width=event.width)
                canvas.configure(scrollregion=canvas.bbox("all"))

            canvas.bind("<Configure>", on_canvas_configure)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            content_frame = tk.Frame(scrollable_frame)
            content_frame.pack(expand=True)

            tk.Label(content_frame, text="👤 Customer Analysis",
                     font=('Arial', 20, 'bold')).pack(pady=20)
            tk.Label(content_frame, text="Select a customer analysis dimension",
                     font=('Arial', 12)).pack(pady=5)

            tk.Frame(content_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            def make_query(sql, title):
                def inner():
                    try:
                        df = query_data(sql)
                        show_table_window(df, title, sortable=True)
                    except Exception as e:
                        messagebox.showerror("Query Error", f"Failed to load data: {e}")

                return inner

            btn_kwargs = {'width': 35, 'height': 2, 'font': ('Arial', 12)}

            tk.Button(content_frame, text="🔍 Search Customers (by Name)",
                      command=search_customer_window,
                      **btn_kwargs).pack(pady=4)

            tk.Frame(content_frame, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=60, pady=5)

            tk.Button(content_frame, text="📋 View All Customers (by ID)",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY customer_id
                      """, "All Customers (by ID)"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="🔤 Sort by Last Name (A-Z)",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY last_name
                      """, "Sort by Last Name (A-Z)"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="🏷️ Sort by Customer Type",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY customer_type
                      """, "Sort by Customer Type"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="🏙️ Sort by City",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY city
                      """, "Sort by City"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="🗺️ Sort by Province",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY province
                      """, "Sort by Province"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="🌍 Sort by Country",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY country
                      """, "Sort by Country"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="📅 Sort by Signup Date (Newest)",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY signup_date DESC
                      """, "Sort by Signup Date (Newest)"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="📅 Sort by Signup Date (Oldest)",
                      command=make_query("""
                          SELECT customer_id, first_name, last_name, email, 
                                 signup_date, customer_type, acquisition_channel,
                                 city, province, country, region_id
                          FROM customers 
                          ORDER BY signup_date
                      """, "Sort by Signup Date (Oldest)"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="📊 Customer Type Distribution",
                      command=make_query("""
                          SELECT customer_type, COUNT(*) as count
                          FROM customers 
                          GROUP BY customer_type 
                          ORDER BY count DESC
                      """, "Customer Type Distribution"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="📊 Acquisition Channel Distribution",
                      command=make_query("""
                          SELECT acquisition_channel, COUNT(*) as count
                          FROM customers 
                          GROUP BY acquisition_channel 
                          ORDER BY count DESC
                      """, "Acquisition Channel Distribution"),
                      **btn_kwargs).pack(pady=4)

            tk.Button(content_frame, text="📊 Customer Count by Province",
                      command=make_query("""
                          SELECT province, COUNT(*) as customer_count
                          FROM customers 
                          GROUP BY province 
                          ORDER BY customer_count DESC
                      """, "Province Customer Count"),
                      **btn_kwargs).pack(pady=4)

            tk.Frame(content_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=40, pady=10)

            tk.Button(content_frame, text="⬅ Back to Main Menu",
                      command=self.show_main_page,
                      width=20, height=1, font=('Arial', 12), bg='#f0f0f0').pack(pady=10)

            tk.Label(content_frame, text="💡 Sort by any column in the table popup",
                     font=('Arial', 9), fg='gray').pack(pady=5)

            tk.Label(content_frame, text="", font=('Arial', 8)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers page: {e}")


# ==================== Main Entry Point ====================
def main():
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()