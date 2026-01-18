# Tool definitions for OpenAI-compatible API (z.ai)
tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_customer",
            "description": "Look up customer information by customer ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer ID (e.g., CUST001)"
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Check the status and details of a specific order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID (e.g., ORD12345)"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_orders",
            "description": "Get all orders for a specific customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer ID"
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Process a refund for a delivered order",
            "parameters": {
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
    }
]
