"""
Shared helper functions for AI Agents
"""
import os
import sqlite3
from typing import Dict, Any
from datetime import datetime, timedelta

# =============================================================================
# DATABASE HELPER FUNCTIONS
# =============================================================================

def init_database(db_name='customer_support.db'):
    """Create and populate the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        tier TEXT NOT NULL,
        balance REAL DEFAULT 0.0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        status TEXT NOT NULL,
        items TEXT NOT NULL,
        total REAL NOT NULL,
        tracking TEXT,
        estimated_delivery TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
    ''')
    
    # Create refunds table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS refunds (
        refund_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        amount REAL NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    )
    ''')
    
    # Insert sample customers
    customers = [
        ('CUST001', 'Sarah Johnson', 'sarah.j@email.com', 'premium', 150.00),
        ('CUST002', 'Mike Chen', 'mike.c@email.com', 'standard', 0.00),
        ('CUST003', 'Emma Williams', 'emma.w@email.com', 'premium', -25.00),
        ('CUST004', 'David Brown', 'david.b@email.com', 'standard', 75.00),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO customers (customer_id, name, email, tier, balance)
    VALUES (?, ?, ?, ?, ?)
    ''', customers)
    
    # Insert sample orders
    orders = [
        ('ORD12345', 'CUST001', 'shipped', 'Laptop, Mouse', 1299.99, 'TRK789456123', '2025-01-25'),
        ('ORD12346', 'CUST002', 'processing', 'Headphones', 199.99, None, '2025-01-28'),
        ('ORD12347', 'CUST003', 'delivered', 'Keyboard, Webcam', 249.99, 'TRK789456124', '2025-01-20'),
        ('ORD12348', 'CUST001', 'delivered', 'Monitor', 399.99, 'TRK789456125', '2025-01-15'),
        ('ORD12349', 'CUST004', 'cancelled', 'Mouse Pad', 15.99, None, None),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO orders (order_id, customer_id, status, items, total, tracking, estimated_delivery)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', orders)

    conn.commit()
    conn.close()


# Interactive Database Explorer
def explore_database():
    """Interactive tool to explore the database"""
    conn = sqlite3.connect('customer_support.db')
    
    print("=" * 60)
    print("DATABASE EXPLORER")
    print("=" * 60)
    
    # Show table schemas
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\n📋 Available Tables:")
    for table in tables:
        table_name = table[0]
        print(f"\n  {table_name.upper()}:")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"    - {col[1]} ({col[2]})")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"    Total records: {count}")
    
    conn.close()


# Clean up Dastabase
def reset_database():
    """Reset the database to original state"""
    if os.path.exists('customer_support.db'):
        os.remove('customer_support.db')
    init_database()
    print("🔄 Database reset complete!")


def lookup_customer(customer_id: str) -> Dict[str, Any]:
    """Look up customer information by ID"""
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT customer_id, name, email, tier, balance
    FROM customers
    WHERE customer_id = ?
    ''', (customer_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "status": "found",
            "customer": {
                "customer_id": row[0],
                "name": row[1],
                "email": row[2],
                "tier": row[3],
                "balance": row[4]
            }
        }
    return {"status": "not_found", "message": "Customer not found"}


def lookup_customer_by_name(name: str) -> Dict[str, Any]:
    """Look up customer information by name (case-insensitive partial match)"""
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT customer_id, name, email, tier, balance
    FROM customers
    WHERE LOWER(name) LIKE LOWER(?)
    ''', (f'%{name}%',))

    rows = cursor.fetchall()
    conn.close()

    if rows:
        customers = []
        for row in rows:
            customers.append({
                "customer_id": row[0],
                "name": row[1],
                "email": row[2],
                "tier": row[3],
                "balance": row[4]
            })
        return {
            "status": "found",
            "count": len(customers),
            "customers": customers
        }
    return {"status": "not_found", "message": "No customers found with that name"}


def check_order_status(order_id: str) -> Dict[str, Any]:
    """Check the status of an order"""
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT o.order_id, o.customer_id, o.status, o.items, o.total, 
           o.tracking, o.estimated_delivery, c.name
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_id = ?
    ''', (order_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "status": "found",
            "order": {
                "order_id": row[0],
                "customer_id": row[1],
                "customer_name": row[7],
                "status": row[2],
                "items": row[3],
                "total": row[4],
                "tracking": row[5],
                "estimated_delivery": row[6]
            }
        }
    return {"status": "not_found", "message": "Order not found"}

    
def get_customer_orders(customer_id: str) -> Dict[str, Any]:
    """Get all orders for a customer"""
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()
    
    # First verify customer exists
    cursor.execute('SELECT name FROM customers WHERE customer_id = ?', (customer_id,))
    customer = cursor.fetchone()
    
    if not customer:
        conn.close()
        return {"status": "error", "message": "Customer not found"}
    
    # Get all orders
    cursor.execute('''
    SELECT order_id, status, items, total, estimated_delivery
    FROM orders
    WHERE customer_id = ?
    ORDER BY created_at DESC
    ''', (customer_id,))
    
    orders = []
    for row in cursor.fetchall():
        orders.append({
            "order_id": row[0],
            "status": row[1],
            "items": row[2],
            "total": row[3],
            "estimated_delivery": row[4]
        })
    
    conn.close()
    
    return {
        "status": "success",
        "customer_name": customer[0],
        "total_orders": len(orders),
        "orders": orders
    }


def process_refund(order_id: str, reason: str) -> Dict[str, Any]:
    """Process a refund for an order"""
    conn = sqlite3.connect('customer_support.db')
    cursor = conn.cursor()
    
    # Check if order exists and can be refunded
    cursor.execute('''
    SELECT order_id, status, total, customer_id
    FROM orders
    WHERE order_id = ?
    ''', (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return {"status": "error", "message": "Order not found"}
    
    order_id, status, total, customer_id = order
    
    if status != "delivered":
        conn.close()
        return {
            "status": "error",
            "message": f"Cannot refund order with status: {status}. Order must be delivered."
        }
    
    # Check if already refunded
    cursor.execute('SELECT refund_id FROM refunds WHERE order_id = ?', (order_id,))
    if cursor.fetchone():
        conn.close()
        return {
            "status": "error",
            "message": "This order has already been refunded"
        }
    
    # Create refund
    refund_id = f"REF{order_id[3:]}"
    cursor.execute('''
    INSERT INTO refunds (refund_id, order_id, amount, reason, status)
    VALUES (?, ?, ?, ?, 'approved')
    ''', (refund_id, order_id, total, reason))
    
    # Update order status
    cursor.execute('''
    UPDATE orders 
    SET status = 'refunded'
    WHERE order_id = ?
    ''', (order_id,))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "refund_id": refund_id,
        "order_id": order_id,
        "amount": total,
        "message": f"Refund of ${total} approved. Refund ID: {refund_id}. Amount will appear in 3-5 business days."
    }


# =============================================================================
# Inventory Database Functions
# =============================================================================
def reset_inventory_database(db_name='inventory.db'):
    """Reset inventory database to original state"""
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"🗑️  Deleted existing database: {db_name}")
    return init_inventory_database(db_name)

    
def init_inventory_database(db_name='inventory.db'):
    """Create and populate inventory database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        reorder_point INTEGER NOT NULL,
        supplier TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create sales history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        date TEXT NOT NULL,
        quantity_sold INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    # Create purchase orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS purchase_orders (
        po_id TEXT PRIMARY KEY,
        product_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_cost REAL,
        total_cost REAL,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    # Insert sample products
    products = [
        ('PROD001', 'Wireless Mouse', 'Electronics', 29.99, 45, 20, 'TechCorp'),
        ('PROD002', 'USB-C Cable', 'Electronics', 12.99, 8, 15, 'TechCorp'),
        ('PROD003', 'Notebook Pack', 'Office Supplies', 8.99, 150, 50, 'OfficeMax'),
        ('PROD004', 'Desk Lamp', 'Furniture', 45.00, 12, 10, 'HomeGoods'),
        ('PROD005', 'Ergonomic Chair', 'Furniture', 299.99, 3, 5, 'HomeGoods'),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO products (product_id, name, category, price, stock, reorder_point, supplier)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Insert sample sales history for last 7 days
    # PROD002 (USB-C Cable) has high demand - will need reordering
    # PROD005 (Chair) has low stock + low demand
    sales_data = []
    
    for day in range(7):
        date = (datetime.now() - timedelta(days=6-day)).strftime('%Y-%m-%d')
        
        # PROD001: Moderate, steady sales
        sales_data.append(('PROD001', date, 5 + (day % 3)))
        
        # PROD002: HIGH sales - this will trigger reorder!
        sales_data.append(('PROD002', date, 10 + day * 2))
        
        # PROD003: Low sales, plenty of stock
        sales_data.append(('PROD003', date, 2 + (day % 3)))
        
        # PROD004: Very low, sporadic sales
        sales_data.append(('PROD004', date, day % 2))
        
        # PROD005: Low sales, but also low stock
        sales_data.append(('PROD005', date, 0 if day % 3 == 0 else 1))
    
    cursor.executemany('''
    INSERT OR IGNORE INTO sales_history (product_id, date, quantity_sold)
    VALUES (?, ?, ?)
    ''', sales_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Inventory database initialized!")
    print("📊 Sample data:")
    print("   - 5 products across 3 categories")
    print("   - 7 days of sales history")
    print("   - PROD002 (USB-C Cable): Low stock + High demand ⚠️")
    print("   - PROD005 (Ergonomic Chair): Low stock + Low demand")
    print()
    
    return f"✅ Database '{db_name}' ready!"