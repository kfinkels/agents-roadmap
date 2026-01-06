# Tool definitions for Claude (LiteLLM)
tools = [
    {
        "type": "custom",  # Add this line
        "name": "lookup_customer",
        "description": "Look up customer information by customer ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID (e.g., CUST001)"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "type": "custom",  # Add this line
        "name": "check_order_status",
        "description": "Check the status and details of a specific order",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID (e.g., ORD12345)"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "type": "custom",  # Add this line
        "name": "get_customer_orders",
        "description": "Get all orders for a specific customer",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "type": "custom",  # Add this line
        "name": "process_refund",
        "description": "Process a refund for a delivered order",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to refund"
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the refund"
                }
            },
            "required": ["order_id", "reason"]
        }
    }
]