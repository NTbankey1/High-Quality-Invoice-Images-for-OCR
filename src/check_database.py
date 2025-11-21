"""
Script để kiểm tra trạng thái database
Người phụ trách: Người 1 - Data Engineer

Cách sử dụng:
python src/check_database.py
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Thêm thư mục src vào sys.path để import config
sys.path.insert(0, str(Path(__file__).parent))

from config import DB_CONFIG, TABLE_ORDERS
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def check_database():
    """Kiểm tra trạng thái database"""
    try:
        # Tạo connection string
        connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        
        logger.info(f"Đang kết nối đến database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
        engine = create_engine(connection_string, echo=False)
        
        with engine.connect() as conn:
            # Kiểm tra connection
            conn.execute(text("SELECT 1"))
            logger.info("✓ Kết nối database thành công")
            
            # Kiểm tra bảng tồn tại (sử dụng parameterized query)
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = :db_name 
                AND table_name = :table_name
            """), {"db_name": DB_CONFIG['database'], "table_name": TABLE_ORDERS})
            
            if result.scalar() > 0:
                logger.info(f"✓ Bảng '{TABLE_ORDERS}' đã tồn tại")
                
                # Đếm số dòng (TABLE_ORDERS là constant nên an toàn)
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM `{TABLE_ORDERS}`"))
                row_count = count_result.scalar()
                logger.info(f"✓ Số dòng trong bảng: {row_count:,}")
                
                # Kiểm tra views (sử dụng parameterized query)
                views_result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.views 
                    WHERE table_schema = :db_name
                """), {"db_name": DB_CONFIG['database']})
                views = [row[0] for row in views_result]
                if views:
                    logger.info(f"✓ Có {len(views)} views: {', '.join(views)}")
                else:
                    logger.warning("⚠ Chưa có views nào")
                
            else:
                logger.warning(f"⚠ Bảng '{TABLE_ORDERS}' chưa tồn tại")
                logger.info("Chạy: python src/setup_database.py để tạo database")
                return False
        
        logger.info("✓ Kiểm tra database hoàn tất!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Lỗi khi kiểm tra database: {str(e)}")
        logger.info("Kiểm tra lại thông tin kết nối trong file .env")
        return False


if __name__ == "__main__":
    success = check_database()
    sys.exit(0 if success else 1)

