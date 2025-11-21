"""
Script để import dữ liệu từ CSV vào MySQL database
Người phụ trách: Người 1 - Data Engineer

Cách sử dụng:
1. Cài đặt dependencies: pip install -r requirements.txt
2. Tạo file .env từ .env.example và cập nhật thông tin database
3. Chạy script: python src/import_to_sql.py

Tùy chọn:
- Thêm --append để append thay vì replace: python src/import_to_sql.py --append
- Thêm --validate để chỉ validate dữ liệu: python src/import_to_sql.py --validate
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import logging

# Thêm thư mục src vào sys.path để import config
sys.path.insert(0, str(Path(__file__).parent))

# Import config
from config import (
    DB_CONFIG, CSV_FILE, TABLE_ORDERS, EXPECTED_COLUMNS,
    DATE_COLUMNS, NUMERIC_COLUMNS, STRING_COLUMNS,
    IMPORT_CHUNKSIZE, IMPORT_METHOD
)

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/import.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database configuration from config.py
DB_HOST = DB_CONFIG['host']
DB_USER = DB_CONFIG['user']
DB_PASSWORD = DB_CONFIG['password']
DB_NAME = DB_CONFIG['database']
DB_PORT = DB_CONFIG['port']

# Use config values (convert Path to string if needed)
CSV_FILE_PATH = str(CSV_FILE) if hasattr(CSV_FILE, '__fspath__') else CSV_FILE
TABLE_NAME = TABLE_ORDERS


def validate_csv_file(file_path):
    """
    Validate CSV file exists and has correct structure
    """
    # Convert Path object to string if needed
    file_path_str = str(file_path) if hasattr(file_path, '__fspath__') else file_path
    
    if not os.path.exists(file_path_str):
        raise FileNotFoundError(f"File không tồn tại: {file_path_str}")
    
    logger.info(f"Đang kiểm tra file: {file_path_str}")
    file_size = os.path.getsize(file_path_str) / (1024 * 1024)  # MB
    logger.info(f"Kích thước file: {file_size:.2f} MB")
    
    return True


def validate_dataframe(df):
    """
    Validate dataframe structure and data quality
    """
    logger.info("Đang validate cấu trúc dữ liệu...")
    
    # Check columns
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    extra_cols = set(df.columns) - set(EXPECTED_COLUMNS)
    
    if missing_cols:
        logger.warning(f"Các cột thiếu: {missing_cols}")
    if extra_cols:
        logger.warning(f"Các cột thêm: {extra_cols}")
    
    # Data quality checks
    total_rows = len(df)
    logger.info(f"Tổng số dòng: {total_rows:,}")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        logger.warning(f"Số dòng trùng lặp: {duplicates:,} ({duplicates/total_rows*100:.2f}%)")
    
    # Check missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        logger.info("Giá trị thiếu theo cột:")
        for col, count in missing_values[missing_values > 0].items():
            logger.info(f"  - {col}: {count:,} ({count/total_rows*100:.2f}%)")
    
    # Check data types
    logger.info("Kiểu dữ liệu:")
    for col in df.columns:
        logger.info(f"  - {col}: {df[col].dtype}")
    
    return True


def convert_date_columns(df):
    """
    Chuyển đổi các cột ngày tháng từ string sang datetime
    """
    logger.info("Đang chuyển đổi các cột ngày tháng...")
    for col in DATE_COLUMNS:
        if col in df.columns:
            before_count = df[col].notna().sum()
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
            after_count = df[col].notna().sum()
            if before_count != after_count:
                logger.warning(f"Cột {col}: {before_count - after_count} giá trị không parse được")
            else:
                logger.info(f"✓ {col}: {after_count:,} giá trị hợp lệ")
    
    return df


def clean_dataframe(df):
    """
    Clean và chuẩn hóa dữ liệu
    """
    logger.info("Đang làm sạch dữ liệu...")
    
    # Remove leading/trailing whitespace from string columns
    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', None)
    
    # Ensure numeric columns are correct type
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            if col == 'price':
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    logger.info("✓ Hoàn thành làm sạch dữ liệu")
    return df


def get_database_engine():
    """
    Tạo và test database connection
    """
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(
        connection_string,
        echo=False,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600     # Recycle connections after 1 hour
    )
    
    # Test connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"✓ Kết nối database thành công: {DB_NAME}@{DB_HOST}")
        return engine
    except Exception as e:
        logger.error(f"✗ Không thể kết nối database: {str(e)}")
        raise


def check_table_exists(engine, table_name):
    """
    Kiểm tra bảng đã tồn tại chưa
    """
    with engine.connect() as conn:
        # Sử dụng parameterized query để tránh SQL injection
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = :db_name 
            AND table_name = :table_name
        """), {"db_name": DB_NAME, "table_name": table_name})
        return result.scalar() > 0


def import_csv_to_sql(append=False, validate_only=False):
    """
    Import dữ liệu từ CSV file vào MySQL database
    """
    start_time = datetime.now()
    
    try:
        # Step 1: Validate CSV file
        validate_csv_file(CSV_FILE_PATH)
        
        # Step 2: Read CSV file
        logger.info(f"Đang đọc file CSV: {CSV_FILE_PATH}")
        df = pd.read_csv(CSV_FILE_PATH, low_memory=False)
        logger.info(f"✓ Đã đọc {len(df):,} dòng dữ liệu")
        logger.info(f"✓ Số cột: {len(df.columns)}")
        
        # Step 3: Validate dataframe
        validate_dataframe(df)
        
        # Step 4: Convert date columns
        df = convert_date_columns(df)
        
        # Step 5: Clean data
        df = clean_dataframe(df)
        
        if validate_only:
            logger.info("✓ Validation hoàn tất - Không import dữ liệu (--validate mode)")
            return
        
        # Step 6: Connect to database
        engine = get_database_engine()
        
        # Step 7: Check if table exists
        table_exists = check_table_exists(engine, TABLE_NAME)
        if_exists_mode = 'append' if append else 'replace'
        
        if table_exists and not append:
            logger.warning(f"Bảng {TABLE_NAME} đã tồn tại. Sẽ được thay thế (replace)")
        elif table_exists and append:
            logger.info(f"Bảng {TABLE_NAME} đã tồn tại. Sẽ thêm dữ liệu mới (append)")
        
        # Step 8: Import to database
        logger.info(f"Đang import dữ liệu vào bảng {TABLE_NAME}...")
        logger.info(f"Mode: {if_exists_mode}")
        logger.info("(Quá trình này có thể mất vài phút tùy vào kích thước dữ liệu)")
        
        # Calculate chunksize based on data size
        chunksize = min(IMPORT_CHUNKSIZE, max(100, len(df) // 100))
        
        # Import với chunksize để xử lý file lớn
        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists=if_exists_mode,
            index=False,
            chunksize=chunksize,
            method=IMPORT_METHOD
        )
        
        logger.info(f"✓ Import thành công {len(df):,} dòng vào bảng {TABLE_NAME}!")
        
        # Step 9: Verify import
        with engine.connect() as conn:
            # TABLE_NAME là constant nên an toàn, nhưng vẫn nên dùng backticks
            result = conn.execute(text(f"SELECT COUNT(*) FROM `{TABLE_NAME}`"))
            count = result.scalar()
            logger.info(f"✓ Tổng số dòng trong database: {count:,}")
            
            # Get sample data
            sample = conn.execute(text(f"SELECT * FROM `{TABLE_NAME}` LIMIT 1"))
            if sample.rowcount > 0:
                logger.info("✓ Dữ liệu đã được import thành công")
        
        # Calculate duration
        duration = datetime.now() - start_time
        logger.info(f"✓ Hoàn thành trong {duration.total_seconds():.2f} giây")
        
    except FileNotFoundError as e:
        logger.error(f"✗ Lỗi file: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Lỗi khi import: {str(e)}", exc_info=True)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Import CSV data to MySQL database')
    parser.add_argument('--append', action='store_true', help='Append data instead of replacing')
    parser.add_argument('--validate', action='store_true', help='Only validate data, do not import')
    args = parser.parse_args()
    
    import_csv_to_sql(append=args.append, validate_only=args.validate)


if __name__ == "__main__":
    main()

