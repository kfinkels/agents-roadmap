import sqlite3
from datetime import datetime
from typing import Any, Dict, List


# =============================================================================
# INVENTORY TOOL DECLARATIONS (for OpenAI-compatible API / z.ai)
# =============================================================================

INVENTORY_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check current stock level for a specific product. Returns stock quantity, reorder point, stock status, and supplier information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID (e.g., PROD001)"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_inventory",
            "description": "Search inventory by category or find low stock items. Can filter by category (Electronics, Office Supplies, Furniture) and/or show only items below reorder point.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by product category: 'Electronics', 'Office Supplies', or 'Furniture'. Leave empty to search all categories."
                    },
                    "low_stock_only": {
                        "type": "boolean",
                        "description": "If true, only return items where current stock is at or below the reorder point. Default is false."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sales_trend",
            "description": "Get sales trend analysis and stockout prediction for a product. Returns last 7 days of sales data, average daily sales, trend direction, and estimated days until stockout. Includes a recommendation on whether to reorder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID (e.g., PROD002)"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_purchase_order",
            "description": "Create a purchase order to restock a product. This will generate a PO with the supplier, calculate costs, and track the order. Use this when a product needs to be restocked.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID to reorder (e.g., PROD002)"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of units to order. Consider average daily sales and lead time (5-7 days) when deciding quantity."
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for the purchase order (e.g., 'Low stock - high demand', 'Approaching stockout', 'Routine reorder')"
                    }
                },
                "required": ["product_id", "quantity", "reason"]
            }
        }
    }
]


# =============================================================================
# INVENTORY TOOL FUNCTIONS
# =============================================================================

def check_stock(product_id: str, db_name='inventory.db') -> Dict[str, Any]:
    """Check current stock level for a product"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT product_id, name, stock, reorder_point, supplier, category, price
    FROM products
    WHERE product_id = ?
    ''', (product_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"status": "error", "message": f"Product {product_id} not found"}
    
    product_id, name, stock, reorder_point, supplier, category, price = row
    
    # Determine stock status
    stock_status = "healthy"
    if stock <= reorder_point:
        stock_status = "low"
    if stock == 0:
        stock_status = "out_of_stock"
    
    return {
        "status": "success",
        "product_id": product_id,
        "product_name": name,
        "category": category,
        "price": price,
        "current_stock": stock,
        "reorder_point": reorder_point,
        "stock_status": stock_status,
        "supplier": supplier
    }


def search_inventory(category: str = None, low_stock_only: bool = False, db_name='inventory.db') -> List[Dict[str, Any]]:
    """Search inventory by category or show low stock items"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = 'SELECT product_id, name, category, price, stock, reorder_point FROM products WHERE 1=1'
    params = []
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    if low_stock_only:
        query += ' AND stock <= reorder_point'
    
    cursor.execute(query, params)
    
    results = []
    for row in cursor.fetchall():
        product_id, name, category, price, stock, reorder_point = row
        
        stock_status = "healthy"
        if stock <= reorder_point:
            stock_status = "low"
        if stock == 0:
            stock_status = "out_of_stock"
        
        results.append({
            "product_id": product_id,
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "reorder_point": reorder_point,
            "stock_status": stock_status
        })
    
    conn.close()
    return results


def get_sales_trend(product_id: str, db_name='inventory.db') -> Dict[str, Any]:
    """Get sales trend analysis for a product"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get product info
    cursor.execute('SELECT name, stock, reorder_point FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return {"status": "error", "message": f"Product {product_id} not found"}
    
    product_name, current_stock, reorder_point = product
    
    # Get sales history (last 7 days, ordered oldest to newest)
    cursor.execute('''
    SELECT date, quantity_sold 
    FROM sales_history 
    WHERE product_id = ? 
    ORDER BY date ASC
    LIMIT 7
    ''', (product_id,))
    
    sales_records = cursor.fetchall()
    conn.close()
    
    if not sales_records:
        return {
            "status": "success",
            "product_id": product_id,
            "product_name": product_name,
            "last_7_days_sales": [],
            "average_daily_sales": 0,
            "trend": "no_data",
            "current_stock": current_stock,
            "reorder_point": reorder_point,
            "estimated_days_until_stockout": 999,
            "recommendation": "No sales data available"
        }
    
    # Extract just the quantities for calculations
    sales_quantities = [record[1] for record in sales_records]
    
    # Calculate average daily sales
    avg_daily = sum(sales_quantities) / len(sales_quantities)
    
    # Calculate days until stockout
    if avg_daily > 0:
        days_remaining = int(current_stock / avg_daily)
    else:
        days_remaining = 999
    
    # Determine trend (comparing first half vs second half of period)
    if len(sales_quantities) >= 4:
        first_half_avg = sum(sales_quantities[:len(sales_quantities)//2]) / (len(sales_quantities)//2)
        second_half_avg = sum(sales_quantities[len(sales_quantities)//2:]) / (len(sales_quantities) - len(sales_quantities)//2)
        
        if second_half_avg > first_half_avg * 1.2:
            trend = "increasing"
        elif second_half_avg < first_half_avg * 0.8:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    # Generate recommendation
    if current_stock <= reorder_point and days_remaining <= 7:
        recommendation = f"URGENT: Reorder needed. Only {days_remaining} days of stock remaining."
    elif current_stock <= reorder_point:
        recommendation = f"Reorder recommended. Stock below reorder point."
    elif days_remaining <= 7:
        recommendation = f"Monitor closely. Will run out in approximately {days_remaining} days."
    else:
        recommendation = "Stock levels adequate."
    
    return {
        "status": "success",
        "product_id": product_id,
        "product_name": product_name,
        "last_7_days_sales": sales_quantities,
        "average_daily_sales": round(avg_daily, 2),
        "trend": trend,
        "current_stock": current_stock,
        "reorder_point": reorder_point,
        "estimated_days_until_stockout": days_remaining,
        "recommendation": recommendation
    }


def create_purchase_order(product_id: str, quantity: int, reason: str, db_name='inventory.db') -> Dict[str, Any]:
    """Create a purchase order to restock a product"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get product details
    cursor.execute('SELECT name, price, supplier FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return {"status": "error", "message": f"Product {product_id} not found"}
    
    product_name, retail_price, supplier = product
    
    # Calculate costs (assume 60% of retail price is our cost)
    unit_cost = retail_price * 0.6
    total_cost = unit_cost * quantity
    
    # Generate PO ID
    po_id = f"PO{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Insert purchase order
    cursor.execute('''
    INSERT INTO purchase_orders (po_id, product_id, quantity, unit_cost, total_cost, reason, status)
    VALUES (?, ?, ?, ?, ?, ?, 'pending')
    ''', (po_id, product_id, quantity, unit_cost, total_cost, reason))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "purchase_order_id": po_id,
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity,
        "unit_cost": round(unit_cost, 2),
        "total_cost": round(total_cost, 2),
        "supplier": supplier,
        "reason": reason,
        "estimated_delivery": "5-7 business days",
        "message": f"Purchase order {po_id} created successfully"
    }