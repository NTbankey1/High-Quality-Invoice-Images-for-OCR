"""
Configuration file cho Data Engineering tasks
Người phụ trách: Người 1 - Data Engineer
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Get project root directory (parent of src directory)
PROJECT_ROOT = Path(__file__).parent.parent

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'foodpanda_db'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

# File paths (sử dụng absolute paths từ project root)
DATA_DIR = PROJECT_ROOT / 'data'
CSV_FILE = DATA_DIR / 'foodpanda_orders.csv'
SQL_SCHEMA_FILE = PROJECT_ROOT / 'sql' / 'schema.sql'
SQL_QUERIES_FILE = PROJECT_ROOT / 'sql' / 'queries.sql'

# Table names
TABLE_ORDERS = 'foodpanda_orders'

# Expected columns
EXPECTED_COLUMNS = [
    'customer_id', 'gender', 'age', 'city', 'signup_date',
    'order_id', 'order_date', 'restaurant_name', 'dish_name', 'category',
    'quantity', 'price', 'payment_method', 'order_frequency',
    'last_order_date', 'loyalty_points', 'churned', 'rating',
    'rating_date', 'delivery_status'
]

# Date columns that need conversion
DATE_COLUMNS = ['signup_date', 'order_date', 'last_order_date', 'rating_date']

# Numeric columns
NUMERIC_COLUMNS = ['quantity', 'price', 'rating', 'loyalty_points', 'order_frequency']

# String columns
STRING_COLUMNS = [
    'customer_id', 'gender', 'age', 'city', 'order_id',
    'restaurant_name', 'dish_name', 'category', 'payment_method',
    'churned', 'delivery_status'
]

# Import settings
IMPORT_CHUNKSIZE = 1000
IMPORT_METHOD = 'multi'

