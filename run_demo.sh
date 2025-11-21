#!/bin/bash
# Script để chạy demo nhanh cho thuyết trình
# High-Quality Invoice Images for OCR

set -e  # Dừng nếu có lỗi

echo "=========================================="
echo "  DEMO SCRIPT - FOODPANDA ANALYTICS"
echo "=========================================="
echo ""

# Màu sắc cho output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Hàm in thông báo
print_step() {
    echo -e "${GREEN}=== $1 ===${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Kiểm tra Python
print_step "BƯỚC 1: Kiểm tra Python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    print_error "Python không được tìm thấy!"
    exit 1
fi
echo "✓ Python: $($PYTHON_CMD --version)"
echo ""

# Kiểm tra MySQL
print_step "BƯỚC 2: Kiểm tra MySQL"
if command -v mysql &> /dev/null; then
    echo "✓ MySQL client đã được cài đặt"
else
    print_warning "MySQL client chưa được cài đặt"
fi
echo ""

# Kiểm tra dependencies
print_step "BƯỚC 3: Kiểm tra dependencies"
REQUIRED_PACKAGES=("pandas" "numpy" "sqlalchemy" "pymysql" "matplotlib" "seaborn" "plotly" "jupyter" "dotenv")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    # Xử lý tên package khác với tên import
    if [ "$package" == "dotenv" ]; then
        import_name="dotenv"
    else
        import_name="$package"
    fi
    
    if ! $PYTHON_CMD -c "import $import_name" 2>/dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    print_warning "Thiếu các packages: ${MISSING_PACKAGES[*]}"
    echo "Đang cài đặt dependencies..."
    if $PYTHON_CMD -m pip install -r requirements.txt; then
        echo "✓ Đã cài đặt dependencies"
    else
        print_error "Không thể cài đặt dependencies. Vui lòng chạy: pip install -r requirements.txt"
        exit 1
    fi
else
    echo "✓ Tất cả dependencies đã được cài đặt"
fi
echo ""

# Kiểm tra file .env
print_step "BƯỚC 4: Kiểm tra cấu hình"
if [ -f ".env" ]; then
    echo "✓ File .env đã tồn tại"
    # Kiểm tra password đã được cập nhật chưa
    if grep -q "your_password_here" .env; then
        print_warning "File .env vẫn chứa 'your_password_here'. Vui lòng cập nhật password MySQL thực tế!"
        echo "Chạy: nano .env (hoặc editor khác) để chỉnh sửa"
        exit 1
    fi
else
    print_warning "File .env chưa tồn tại. Vui lòng tạo file .env với thông tin database."
    echo "Tạo file .env mẫu..."
    cat > .env << EOF
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=foodpanda_db
DB_PORT=3306
EOF
    print_warning "Đã tạo file .env mẫu. Vui lòng cập nhật password MySQL của bạn!"
    exit 1
fi
echo ""

# Kiểm tra file CSV
print_step "BƯỚC 5: Kiểm tra dữ liệu"
if [ -f "data/foodpanda_orders.csv" ]; then
    FILE_SIZE=$(du -h data/foodpanda_orders.csv | cut -f1)
    LINE_COUNT=$(wc -l < data/foodpanda_orders.csv)
    echo "✓ File CSV đã tồn tại"
    echo "  - Kích thước: $FILE_SIZE"
    echo "  - Số dòng: $LINE_COUNT"
else
    print_error "File data/foodpanda_orders.csv không tồn tại!"
    print_warning "Vui lòng tải dataset từ Kaggle và đặt vào thư mục data/"
    exit 1
fi
echo ""

# Kiểm tra database
print_step "BƯỚC 6: Kiểm tra database"
cd src
if $PYTHON_CMD check_database.py 2>/dev/null; then
    echo "✓ Database đã được setup"
else
    print_warning "Database chưa được setup. Đang setup database..."
    if $PYTHON_CMD setup_database.py; then
        echo "✓ Database đã được setup thành công"
    else
        print_error "Không thể setup database. Vui lòng kiểm tra lại!"
        exit 1
    fi
fi
cd ..
echo ""

# Kiểm tra dữ liệu đã import chưa
print_step "BƯỚC 7: Kiểm tra dữ liệu trong database"
cd src
DB_CHECK_OUTPUT=$($PYTHON_CMD check_database.py 2>&1)
ROW_COUNT=$(echo "$DB_CHECK_OUTPUT" | grep "Số dòng trong bảng" | grep -oE '[0-9,]+' | tr -d ',' | head -1)
if [ -z "$ROW_COUNT" ]; then
    ROW_COUNT=0
fi

if [ "$ROW_COUNT" -gt 0 ]; then
    echo "✓ Database đã có dữ liệu ($ROW_COUNT dòng)"
    echo ""
    read -p "Bạn có muốn import lại dữ liệu không? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Đang import dữ liệu (có thể mất vài phút)..."
        if $PYTHON_CMD import_to_sql.py; then
            echo "✓ Import dữ liệu thành công"
        else
            print_error "Import dữ liệu thất bại!"
            exit 1
        fi
    fi
else
    print_warning "Database chưa có dữ liệu. Đang import dữ liệu..."
    if $PYTHON_CMD import_to_sql.py; then
        echo "✓ Import dữ liệu thành công"
    else
        print_error "Import dữ liệu thất bại!"
        exit 1
    fi
fi
cd ..
echo ""

# Tóm tắt
print_step "TÓM TẮT"
echo "✓ Môi trường đã sẵn sàng"
echo "✓ Database đã được setup"
echo "✓ Dữ liệu đã được import"
echo ""
echo "=========================================="
echo "  BẠN CÓ THỂ BẮT ĐẦU DEMO!"
echo "=========================================="
echo ""
echo "Các lệnh hữu ích:"
echo "  1. Kiểm tra database:"
echo "     cd src && python check_database.py"
echo ""
echo "  2. Mở Jupyter Notebook:"
echo "     jupyter notebook src/visualization.ipynb"
echo "     jupyter notebook src/analysis.ipynb"
echo ""
echo "  3. Chạy SQL queries:"
echo "     mysql -u root -p foodpanda_db"
echo ""
echo "  4. Xem log files:"
echo "     tail -f logs/import.log"
echo "     tail -f logs/setup.log"
echo ""

