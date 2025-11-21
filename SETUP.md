# HƯỚNG DẪN SETUP DỰ ÁN
## High-Quality Invoice Images for OCR

**Tài liệu này hướng dẫn chi tiết cách setup và chạy dự án từ đầu.**

---

## 📋 YÊU CẦU HỆ THỐNG

### Phần mềm cần thiết

1. **Python 3.8+**
   ```bash
   python --version
   # Hoặc
   python3 --version
   ```

2. **MySQL 8.0+**
   ```bash
   mysql --version
   ```

3. **pip** (Python package manager)
   ```bash
   pip --version
   ```

4. **Git** (tùy chọn, để clone repository)
   ```bash
   git --version
   ```

---

## 🚀 CÁC BƯỚC SETUP

### BƯỚC 1: CÀI ĐẶT PYTHON VÀ DEPENDENCIES

#### 1.1. Kiểm tra Python
```bash
python --version
# Kết quả mong đợi: Python 3.8.x hoặc cao hơn
```

Nếu chưa có Python, cài đặt:
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

- **macOS:**
  ```bash
  brew install python3
  ```

- **Windows:**
  - Download từ [python.org](https://www.python.org/downloads/)
  - Nhớ chọn "Add Python to PATH" khi cài đặt

#### 1.2. Tạo virtual environment (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### 1.3. Cài đặt dependencies
```bash
# Đảm bảo đang ở thư mục gốc của dự án
cd /home/ntbankey/High-Quality-Invoice-Images-for-OCR

# Cài đặt tất cả packages
pip install -r requirements.txt
```

**Kiểm tra cài đặt thành công:**
```bash
pip list | grep -E "pandas|numpy|sqlalchemy|pymysql|matplotlib|seaborn|plotly|jupyter"
```

**⚠️ LƯU Ý QUAN TRỌNG:**
- Nếu gặp lỗi `ModuleNotFoundError: No module named 'pymysql'`, chạy:
  ```bash
  pip install pymysql
  ```
- Hoặc cài đặt lại tất cả dependencies:
  ```bash
  pip install -r requirements.txt --upgrade
  ```

---

### BƯỚC 2: CÀI ĐẶT VÀ CẤU HÌNH MYSQL

#### 2.1. Cài đặt MySQL

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
```

**macOS:**
```bash
brew install mysql
```

**Windows:**
- Download từ [MySQL website](https://dev.mysql.com/downloads/mysql/)
- Chạy installer và làm theo hướng dẫn

#### 2.2. Khởi động MySQL service

**Linux:**
```bash
sudo systemctl start mysql
sudo systemctl enable mysql  # Tự động khởi động khi boot
```

**macOS:**
```bash
brew services start mysql
```

**Windows:**
- Mở Services (services.msc)
- Tìm "MySQL" và Start service

#### 2.3. Thiết lập MySQL root password (nếu chưa có)

**Linux:**
```bash
sudo mysql_secure_installation
```

**macOS/Windows:**
- Sử dụng MySQL Workbench hoặc command line:
```bash
mysql -u root -p
```

Sau đó trong MySQL:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

#### 2.4. Kiểm tra MySQL đang chạy
```bash
# Kiểm tra service
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Hoặc kiểm tra kết nối
mysql -u root -p -e "SELECT VERSION();"
```

---

### BƯỚC 3: CẤU HÌNH FILE .ENV

#### 3.1. Tạo file .env từ template

```bash
# Copy file .env.example thành .env
cp .env.example .env
```

#### 3.2. Cập nhật thông tin trong file .env

Mở file `.env` bằng editor:
```bash
nano .env
# hoặc
vim .env
# hoặc dùng editor khác (VS Code, Notepad++, etc.)
```

**Nội dung file .env:**
```env
# Database Configuration
# Copy this file to .env and update with your actual database credentials

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=foodpanda_db
DB_PORT=3306
```

**Cập nhật các giá trị:**
- `DB_HOST`: Thường là `localhost` (nếu MySQL chạy trên cùng máy)
- `DB_USER`: Thường là `root` (hoặc user MySQL khác)
- `DB_PASSWORD`: **QUAN TRỌNG** - Thay `your_password_here` bằng password MySQL thực tế của bạn
- `DB_NAME`: Tên database (mặc định: `foodpanda_db`)
- `DB_PORT`: Port MySQL (mặc định: `3306`)

**Ví dụ file .env đã cấu hình:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=MySecurePassword123
DB_NAME=foodpanda_db
DB_PORT=3306
```

#### 3.3. Kiểm tra file .env

```bash
# Kiểm tra file đã được tạo
ls -la .env

# Xem nội dung (không hiển thị password nếu lo ngại bảo mật)
cat .env | grep -v PASSWORD
```

**⚠️ LƯU Ý BẢO MẬT:**
- File `.env` chứa thông tin nhạy cảm, **KHÔNG** commit vào Git
- File `.env` đã được thêm vào `.gitignore`
- Không chia sẻ file `.env` với người khác

---

### BƯỚC 4: CHUẨN BỊ DỮ LIỆU

#### 4.1. Tải dataset từ Kaggle

1. Truy cập: [Foodpanda Order & Delivery Trends](https://www.kaggle.com/datasets/...)
2. Download file CSV
3. Đặt file vào thư mục `data/` với tên `foodpanda_orders.csv`

**Hoặc sử dụng command line:**
```bash
# Đảm bảo thư mục data tồn tại
mkdir -p data

# Copy file CSV vào thư mục data/
# (Thay đường dẫn bằng đường dẫn thực tế của file bạn đã tải)
cp /path/to/downloaded/file.csv data/foodpanda_orders.csv
```

#### 4.2. Kiểm tra file CSV

```bash
# Kiểm tra file tồn tại
ls -lh data/foodpanda_orders.csv

# Kiểm tra số dòng
wc -l data/foodpanda_orders.csv

# Xem 5 dòng đầu
head -5 data/foodpanda_orders.csv
```

**Kết quả mong đợi:**
- File có kích thước khoảng 800KB - 1MB
- Có khoảng 6000+ dòng dữ liệu
- Có các cột: customer_id, order_id, restaurant_name, price, etc.

---

### BƯỚC 5: SETUP DATABASE

#### 5.1. Chạy script setup database

```bash
# Đảm bảo đang ở thư mục gốc của dự án
cd /home/ntbankey/High-Quality-Invoice-Images-for-OCR

# Chạy script setup
python src/setup_database.py
```

**Kết quả mong đợi:**
```
Đang kết nối đến MySQL server...
✓ Kết nối MySQL server thành công
Đang đọc file schema: /path/to/sql/schema.sql
Tìm thấy X câu lệnh SQL
Đang thực thi câu lệnh 1/X...
✓ Câu lệnh 1 thành công
...
✓ Setup database hoàn tất!
✓ Database 'foodpanda_db' có X bảng
```

#### 5.2. Kiểm tra database đã setup

```bash
python src/check_database.py
```

**Kết quả mong đợi:**
```
✓ Kết nối database thành công: foodpanda_db@localhost
✓ Bảng 'foodpanda_orders' đã tồn tại
✓ Số dòng trong bảng: 0
✓ Các views đã tạo:
  - vw_daily_orders
  - vw_restaurant_stats
  - vw_customer_stats
```

---

### BƯỚC 6: IMPORT DỮ LIỆU

#### 6.1. Validate dữ liệu (Tùy chọn)

```bash
python src/import_to_sql.py --validate
```

**Kết quả mong đợi:**
```
Đang kiểm tra file: /path/to/data/foodpanda_orders.csv
Kích thước file: X.XX MB
Đang đọc file CSV...
✓ Đã đọc X,XXX dòng dữ liệu
✓ Số cột: XX
Đang validate cấu trúc dữ liệu...
Tổng số dòng: X,XXX
...
✓ Validation hoàn tất - Không import dữ liệu (--validate mode)
```

#### 6.2. Import dữ liệu vào database

```bash
python src/import_to_sql.py
```

**Kết quả mong đợi:**
```
Đang kiểm tra file: /path/to/data/foodpanda_orders.csv
...
Đang đọc file CSV...
✓ Đã đọc X,XXX dòng dữ liệu
...
Đang chuyển đổi các cột ngày tháng...
✓ order_date: X,XXX giá trị hợp lệ
...
Đang làm sạch dữ liệu...
✓ Hoàn thành làm sạch dữ liệu
✓ Kết nối database thành công: foodpanda_db@localhost
Đang import dữ liệu vào bảng foodpanda_orders...
Mode: replace
(Quá trình này có thể mất vài phút tùy vào kích thước dữ liệu)
✓ Import thành công X,XXX dòng vào bảng foodpanda_orders!
✓ Tổng số dòng trong database: X,XXX
✓ Dữ liệu đã được import thành công
✓ Hoàn thành trong XX.XX giây
```

#### 6.3. Verify import

```bash
python src/check_database.py
```

**Kết quả mong đợi:**
```
✓ Kết nối database thành công: foodpanda_db@localhost
✓ Bảng 'foodpanda_orders' đã tồn tại
✓ Số dòng trong bảng: X,XXX  # Số dòng > 0
```

---

## ✅ KIỂM TRA SETUP HOÀN TẤT

### Checklist

- [ ] Python 3.8+ đã được cài đặt
- [ ] MySQL 8.0+ đã được cài đặt và đang chạy
- [ ] Virtual environment đã được tạo và kích hoạt (nếu dùng)
- [ ] Tất cả dependencies đã được cài đặt (`pip install -r requirements.txt`)
- [ ] File `.env` đã được tạo và cấu hình đúng
- [ ] File CSV `data/foodpanda_orders.csv` đã có sẵn
- [ ] Database đã được setup (`python src/setup_database.py`)
- [ ] Dữ liệu đã được import (`python src/import_to_sql.py`)
- [ ] Database có dữ liệu (số dòng > 0)

### Test nhanh

```bash
# Chạy script tự động kiểm tra
./run_demo.sh
```

---

## 🔧 TROUBLESHOOTING

### Lỗi: "Can't connect to MySQL server"

**Nguyên nhân:**
- MySQL service chưa chạy
- Thông tin trong `.env` sai
- User không có quyền

**Giải pháp:**
```bash
# 1. Kiểm tra MySQL service
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# 2. Khởi động MySQL
sudo systemctl start mysql  # Linux
brew services start mysql  # macOS

# 3. Kiểm tra file .env
cat .env

# 4. Test kết nối thủ công
mysql -u root -p -e "SELECT 1;"
```

### Lỗi: "Access denied for user 'root'@'localhost'"

**Nguyên nhân:**
- Password trong `.env` sai
- User không có quyền

**Giải pháp:**
```bash
# 1. Kiểm tra password trong .env
cat .env | grep DB_PASSWORD

# 2. Test kết nối với password
mysql -u root -p
# Nhập password khi được hỏi

# 3. Nếu quên password, reset:
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';
FLUSH PRIVILEGES;
```

### Lỗi: "ModuleNotFoundError: No module named 'config'"

**Nguyên nhân:**
- Đang chạy script từ thư mục sai
- Virtual environment chưa được kích hoạt

**Giải pháp:**
```bash
# 1. Đảm bảo đang ở thư mục gốc
cd /home/ntbankey/High-Quality-Invoice-Images-for-OCR

# 2. Kích hoạt virtual environment (nếu dùng)
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# 3. Chạy lại script
python src/setup_database.py
```

### Lỗi: "File không tồn tại: data/foodpanda_orders.csv"

**Nguyên nhân:**
- File CSV chưa được đặt vào thư mục `data/`
- Tên file sai

**Giải pháp:**
```bash
# 1. Kiểm tra thư mục data
ls -la data/

# 2. Kiểm tra tên file (phải là foodpanda_orders.csv)
ls -la data/*.csv

# 3. Nếu file có tên khác, đổi tên:
mv data/your_file.csv data/foodpanda_orders.csv
```

---

## 📚 TÀI LIỆU THAM KHẢO

- **Hướng dẫn chạy dự án:** `reports/huong_dan_chay_du_an.md`
- **Tài liệu thuyết trình:** `reports/presentation_guide.md`
- **Quick reference:** `reports/quick_reference.md`
- **README chính:** `README.md`

---

## 🎯 BƯỚC TIẾP THEO

Sau khi setup xong, bạn có thể:

1. **Chạy Data Cleaning:**
   ```bash
   jupyter notebook src/data_cleaning.ipynb
   ```

2. **Chạy Data Analysis:**
   ```bash
   jupyter notebook src/analysis.ipynb
   ```

3. **Chạy Data Visualization:**
   ```bash
   jupyter notebook src/visualization.ipynb
   ```

4. **Chạy SQL Queries:**
   ```bash
   mysql -u root -p foodpanda_db < sql/queries.sql
   ```

---

**Chúc bạn setup thành công! 🎉**

