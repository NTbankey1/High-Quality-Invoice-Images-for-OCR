"""
Script để setup database tự động
Người phụ trách: Người 1 - Data Engineer

Cách sử dụng:
python src/setup_database.py
"""

import os
import sys
from pathlib import Path

# Thêm thư mục src vào sys.path để import config
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from config import DB_CONFIG, SQL_SCHEMA_FILE, PROJECT_ROOT
import logging

# Setup logging với absolute path
logs_dir = PROJECT_ROOT / 'logs'
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / 'setup.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(log_file)),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def read_sql_file(file_path):
    """Đọc file SQL và trả về danh sách các câu lệnh"""
    try:
        # Convert Path object to string if needed
        if hasattr(file_path, '__fspath__') or hasattr(file_path, 'resolve'):
            file_path = str(file_path)
        elif not isinstance(file_path, str):
            file_path = str(file_path)
        
        # Resolve absolute path
        file_path = os.path.abspath(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tách các câu lệnh SQL (xử lý cả multi-line statements)
        statements = []
        current_statement = []
        
        for line in content.split('\n'):
            stripped_line = line.strip()
            
            # Bỏ qua comment lines
            if stripped_line.startswith('--'):
                continue
            
            # Bỏ qua empty lines
            if not stripped_line:
                continue
            
            # Thêm line vào current statement
            current_statement.append(stripped_line)
            
            # Kiểm tra nếu kết thúc statement (có dấu ;)
            if stripped_line.endswith(';'):
                statement = ' '.join(current_statement)
                # Loại bỏ dấu ; cuối cùng
                statement = statement.rstrip(';').strip()
                if statement:
                    statements.append(statement)
                current_statement = []
        
        # Nếu còn statement chưa kết thúc (không có dấu ;)
        if current_statement:
            statement = ' '.join(current_statement).strip()
            if statement:
                statements.append(statement)
        
        return statements
    except FileNotFoundError:
        logger.error(f"File không tồn tại: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Lỗi khi đọc file SQL: {str(e)}")
        return []


def setup_database():
    """Setup database và tạo schema"""
    try:
        # Tạo connection string (không có database name để tạo database)
        connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
        
        logger.info("Đang kết nối đến MySQL server...")
        engine = create_engine(connection_string, echo=False)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ Kết nối MySQL server thành công")
        
        # Đọc và thực thi schema.sql
        logger.info(f"Đang đọc file schema: {SQL_SCHEMA_FILE}")
        statements = read_sql_file(SQL_SCHEMA_FILE)
        
        if not statements:
            logger.error("Không tìm thấy câu lệnh SQL nào trong file schema")
            return False
        
        logger.info(f"Tìm thấy {len(statements)} câu lệnh SQL")
        
        # Thực thi từng câu lệnh
        with engine.connect() as conn:
            for i, statement in enumerate(statements, 1):
                try:
                    logger.info(f"Đang thực thi câu lệnh {i}/{len(statements)}...")
                    conn.execute(text(statement))
                    conn.commit()
                    logger.info(f"✓ Câu lệnh {i} thành công")
                except Exception as e:
                    logger.warning(f"⚠ Câu lệnh {i} có lỗi: {str(e)}")
                    # Tiếp tục với câu lệnh tiếp theo
        
        logger.info("✓ Setup database hoàn tất!")
        
        # Kiểm tra database đã được tạo
        with engine.connect() as conn:
            # Sử dụng parameterized query để tránh SQL injection
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = :db_name
            """), {"db_name": DB_CONFIG['database']})
            table_count = result.scalar()
            logger.info(f"✓ Database '{DB_CONFIG['database']}' có {table_count} bảng")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Lỗi khi setup database: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)

