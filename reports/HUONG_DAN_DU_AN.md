# HƯỚNG DẪN DỰ ÁN - TÀI LIỆU TỔNG HỢP
## High-Quality Invoice Images for OCR - Foodpanda Analytics

**Ngày cập nhật:** 2025-01-27  
**Phiên bản:** 1.0

---

## 📋 MỤC LỤC

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Kiến trúc hệ thống](#2-kiến-trúc-hệ-thống)
3. [Hướng dẫn setup](#3-hướng-dẫn-setup)
4. [Hướng dẫn chạy dự án](#4-hướng-dẫn-chạy-dự-án)
5. [Hướng dẫn SQL](#5-hướng-dẫn-sql)
6. [Báo cáo phân tích](#6-báo-cáo-phân-tích)
7. [Hướng dẫn thuyết trình](#7-hướng-dẫn-thuyết-trình)
8. [Quick Reference](#8-quick-reference)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1. Mục tiêu dự án

**"High-Quality Invoice Images for OCR"** là một dự án mô phỏng quy trình tự động hóa xử lý dữ liệu hóa đơn (Invoice / Order) trong doanh nghiệp. Dự án tập trung vào việc:

- ✅ **Thu thập dữ liệu** từ nguồn bên ngoài (Kaggle)
- ✅ **Tiền xử lý và làm sạch** dữ liệu
- ✅ **Lưu trữ** dữ liệu vào database có cấu trúc
- ✅ **Phân tích** dữ liệu để tìm insights
- ✅ **Trực quan hóa** dữ liệu bằng biểu đồ và dashboard
- ✅ **Hỗ trợ** các hệ thống OCR, AI hoặc phân tích tài chính

### 1.2. Nguồn dữ liệu

- **Dataset:** Foodpanda Order & Delivery Trends
- **Nguồn:** Kaggle
- **Định dạng:** CSV
- **Nội dung:** Dữ liệu đơn hàng từ ứng dụng giao đồ ăn Foodpanda

### 1.3. Đội ngũ thực hiện

| Thành viên | Vai trò | Nhiệm vụ chính | Công cụ chính |
|------------|---------|----------------|---------------|
| **Nguyễn Thái Bảo** | Data Engineer (Trưởng nhóm) | Database design, ETL pipeline, Infrastructure | MySQL, Python, SQLAlchemy |
| **Nguyễn Hữu Dương** | Data Cleaning Specialist | Data preprocessing, Quality assurance | Jupyter Notebook, Pandas, NumPy |
| **Nguyễn Thanh Hải** | Data Analyst | Statistical analysis, Pattern discovery | Jupyter Notebook, Pandas, SciPy |
| **Nguyễn Quốc Cường** | Data Visualization | Charts, Dashboards, Interactive visualizations | Matplotlib, Seaborn, Plotly |
| **Nguyễn Đình Trí** | Report & Documentation | Documentation, Reports, Presentation | Markdown, PowerPoint |

---

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1. Sơ đồ tổng quan

```
┌─────────────────┐
│   Kaggle CSV    │
│   (Raw Data)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Import    │  ← Data Engineer
│  (ETL Pipeline) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MySQL Database │
│  (Structured)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ Data   │ │  SQL     │
│Cleaning│ │ Queries  │
└───┬────┘ └────┬─────┘
    │           │
    ▼           ▼
┌─────────────────┐
│  Cleaned Data   │
│     (CSV)       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│Analysis│ │Visualization │
│(Stats) │ │  (Charts)    │
└───┬────┘ └──────┬───────┘
    │             │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │   Reports    │
    │ & Insights   │
    └──────────────┘
```

### 2.2. Cấu trúc thư mục

```
foodpanda-analytics/
│
├── data/                          # Dữ liệu
│   ├── foodpanda_orders.csv      # Raw data
│   └── foodpanda_orders_cleaned.csv  # Cleaned data
│
├── src/                           # Source code
│   ├── config.py                 # Configuration
│   ├── setup_database.py         # Database setup
│   ├── check_database.py         # Database check
│   ├── import_to_sql.py          # ETL pipeline
│   ├── data_cleaning.ipynb       # Data cleaning
│   ├── analysis.ipynb            # Data analysis
│   └── visualization.ipynb       # Data visualization
│
├── sql/                           # SQL scripts
│   ├── schema.sql                # Database schema
│   └── queries.sql               # Analysis queries
│
├── reports/                       # Reports
│   └── HUONG_DAN_DU_AN.md        # Tài liệu này
│
├── logs/                          # Log files
│   └── README.md
│
├── README.md                      # Project documentation
└── requirements.txt               # Dependencies
```

### 2.3. Database Schema

#### Bảng chính: `foodpanda_orders`

**Thông tin khách hàng:**
- `customer_id` (VARCHAR) - ID khách hàng
- `gender` (VARCHAR) - Giới tính
- `age` (VARCHAR) - Độ tuổi
- `city` (VARCHAR) - Thành phố
- `signup_date` (DATE) - Ngày đăng ký

**Thông tin đơn hàng:**
- `order_id` (VARCHAR) - ID đơn hàng
- `order_date` (DATE) - Ngày đặt hàng
- `restaurant_name` (VARCHAR) - Tên nhà hàng
- `dish_name` (VARCHAR) - Tên món ăn
- `category` (VARCHAR) - Danh mục món ăn
- `quantity` (INT) - Số lượng
- `price` (DECIMAL) - Giá tiền
- `payment_method` (VARCHAR) - Phương thức thanh toán

**Thông tin khách hàng thân thiết:**
- `order_frequency` (INT) - Tần suất đặt hàng
- `last_order_date` (DATE) - Ngày đặt hàng cuối
- `loyalty_points` (INT) - Điểm tích lũy
- `churned` (VARCHAR) - Trạng thái rời bỏ

**Đánh giá và giao hàng:**
- `rating` (INT) - Đánh giá (1-5)
- `rating_date` (DATE) - Ngày đánh giá
- `delivery_status` (VARCHAR) - Trạng thái giao hàng

**Metadata:**
- `id` (INT, PRIMARY KEY) - ID tự động
- `created_at` (TIMESTAMP) - Thời gian tạo
- `updated_at` (TIMESTAMP) - Thời gian cập nhật

#### Views

**1. `vw_daily_orders`** - Tổng hợp đơn hàng theo ngày
- Tổng số đơn hàng
- Tổng số khách hàng
- Tổng số items
- Tổng doanh thu
- Giá trị đơn hàng trung bình

**2. `vw_restaurant_stats`** - Thống kê theo nhà hàng
- Tổng số đơn hàng
- Tổng số khách hàng
- Tổng số items bán được
- Tổng doanh thu
- Giá trị đơn hàng trung bình
- Đánh giá trung bình

**3. `vw_customer_stats`** - Thống kê khách hàng
- Tổng số đơn hàng
- Tổng chi tiêu
- Giá trị đơn hàng trung bình
- Ngày đặt hàng cuối
- Điểm tích lũy
- Trạng thái churned

### 2.4. Công nghệ sử dụng

**Backend & Database:**
- Python 3.8+, MySQL 8.0+
- SQLAlchemy 2.0+, PyMySQL 1.0+
- python-dotenv 1.0+

**Data Processing:**
- Pandas 1.5+, NumPy 1.23+

**Visualization:**
- Matplotlib 3.6+, Seaborn 0.12+, Plotly 5.14+

**Development:**
- Jupyter Notebook 6.5+, IPython Kernel 6.20+

---

## 3. HƯỚNG DẪN SETUP

### 3.1. Yêu cầu hệ thống

- **Python 3.8+**
- **MySQL 8.0+**
- **pip** (Python package manager)
- **Git** (tùy chọn)

### 3.2. Cài đặt Python và Dependencies

#### 3.2.1. Kiểm tra Python
```bash
python --version
# Kết quả mong đợi: Python 3.8.x hoặc cao hơn
```

#### 3.2.2. Tạo virtual environment (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### 3.2.3. Cài đặt dependencies
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

### 3.3. Cài đặt và cấu hình MySQL

#### 3.3.1. Cài đặt MySQL

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

#### 3.3.2. Khởi động MySQL service

**Linux:**
```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

**macOS:**
```bash
brew services start mysql
```

#### 3.3.3. Thiết lập MySQL root password
```bash
sudo mysql_secure_installation
```

### 3.4. Cấu hình file .env

#### 3.4.1. Tạo file .env

**Cách 1: Copy từ template (nếu có)**
```bash
cp .env.example .env
```

**Cách 2: Tạo file mới**
```bash
cat > .env << EOF
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=foodpanda_db
DB_PORT=3306
EOF
```

#### 3.4.2. Cập nhật thông tin trong file .env

**Nội dung file .env:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=foodpanda_db
DB_PORT=3306
```

**⚠️ LƯU Ý BẢO MẬT:**
- File `.env` chứa thông tin nhạy cảm, **KHÔNG** commit vào Git
- File `.env` đã được thêm vào `.gitignore`
- Không chia sẻ file `.env` với người khác

### 3.5. Chuẩn bị dữ liệu

#### 3.5.1. Tải dataset từ Kaggle
1. Truy cập: [Foodpanda Order & Delivery Trends](https://www.kaggle.com/datasets/...)
2. Download file CSV
3. Đặt file vào thư mục `data/` với tên `foodpanda_orders.csv`

#### 3.5.2. Kiểm tra file CSV
```bash
# Kiểm tra file tồn tại
ls -lh data/foodpanda_orders.csv

# Kiểm tra số dòng
wc -l data/foodpanda_orders.csv

# Xem 5 dòng đầu
head -5 data/foodpanda_orders.csv
```

### 3.6. Setup Database

#### 3.6.1. Chạy script setup database
```bash
cd /home/ntbankey/High-Quality-Invoice-Images-for-OCR
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

#### 3.6.2. Kiểm tra database đã setup
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

## 4. HƯỚNG DẪN CHẠY DỰ ÁN

### 4.1. Checklist trước khi chạy

#### ✅ Chuẩn bị môi trường
- [ ] Python 3.8+ đã được cài đặt
- [ ] MySQL 8.0+ đã được cài đặt và đang chạy
- [ ] MySQL service đang chạy (`sudo systemctl status mysql`)
- [ ] Virtual environment đã được tạo và kích hoạt (nếu dùng)
- [ ] Tất cả dependencies đã được cài đặt (`pip install -r requirements.txt`)
- [ ] File `.env` đã được tạo và cấu hình đúng
- [ ] File CSV `data/foodpanda_orders.csv` đã có sẵn

#### ✅ Kiểm tra dự án
- [ ] Database đã được setup (`python src/setup_database.py`)
- [ ] Dữ liệu đã được import vào database (`python src/import_to_sql.py`)
- [ ] Cleaned data đã được tạo (`data/foodpanda_orders_cleaned.csv`)
- [ ] Các notebooks đã được chạy và có output
- [ ] Jupyter Notebook đã được cài đặt và có thể chạy

### 4.2. Quy trình chạy dự án từ đầu

#### BƯỚC 1: Import dữ liệu

##### 4.2.1. Validate dữ liệu trước (Tùy chọn)
```bash
python src/import_to_sql.py --validate
```

##### 4.2.2. Import dữ liệu vào database
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
✓ Import thành công X,XXX dòng vào bảng foodpanda_orders!
✓ Tổng số dòng trong database: X,XXX
✓ Dữ liệu đã được import thành công
```

##### 4.2.3. Verify import
```bash
python src/check_database.py
```

#### BƯỚC 2: Data Cleaning

##### 4.2.4. Mở Jupyter Notebook
```bash
jupyter notebook src/data_cleaning.ipynb
```

##### 4.2.5. Chạy các cells trong notebook
1. **Cell 1:** Import libraries và load data
2. **Cell 2:** Kiểm tra dữ liệu ban đầu (shape, info, describe)
3. **Cell 3:** Xử lý missing values
4. **Cell 4:** Xử lý duplicates
5. **Cell 5:** Xử lý outliers
6. **Cell 6:** Chuẩn hóa format
7. **Cell 7:** Export cleaned data

**Kết quả mong đợi:**
- File `data/foodpanda_orders_cleaned.csv` được tạo
- Số dòng cleaned data < số dòng raw data (sau khi xử lý)

#### BƯỚC 3: Data Analysis

##### 4.2.6. Mở Jupyter Notebook
```bash
jupyter notebook src/analysis.ipynb
```

##### 4.2.7. Chạy các cells phân tích
1. **Cell 1:** Load cleaned data
2. **Cell 2:** Thống kê mô tả
3. **Cell 3:** Phân tích phân phối
4. **Cell 4:** Phân tích tương quan
5. **Cell 5:** Phân tích patterns
6. **Cell 6:** Phân tích churn
7. **Cell 7:** Tổng hợp insights

#### BƯỚC 4: Data Visualization

##### 4.2.8. Mở Jupyter Notebook
```bash
jupyter notebook src/visualization.ipynb
```

##### 4.2.9. Chạy các cells visualization
1. **Cell 1:** Load data và setup
2. **Cell 2:** Histogram
3. **Cell 3:** Boxplot
4. **Cell 4:** Scatter plot
5. **Cell 5:** Heatmap
6. **Cell 6:** Time series
7. **Cell 7:** Interactive charts
8. **Cell 8:** Dashboard

### 4.3. Demo trong buổi thuyết trình

#### Demo 1: ETL Pipeline (5 phút)
1. Mở terminal
2. Chạy: `python src/import_to_sql.py --validate`
3. Chạy: `python src/import_to_sql.py`
4. Kiểm tra: `python src/check_database.py`

#### Demo 2: Database Queries (3 phút)
1. Mở MySQL client: `mysql -u root -p foodpanda_db`
2. Chạy: `DESCRIBE foodpanda_orders;`
3. Chạy: `SELECT * FROM vw_daily_orders LIMIT 5;`
4. Chạy: `SELECT * FROM vw_restaurant_stats LIMIT 5;`

#### Demo 3: Data Visualization (5 phút)
1. Mở Jupyter Notebook: `jupyter notebook src/visualization.ipynb`
2. Chạy cell đầu tiên (load data)
3. Chạy cell tạo histogram
4. Chạy cell tạo time series
5. Chạy cell tạo interactive chart

#### Demo 4: Data Analysis (3 phút)
1. Mở Jupyter Notebook: `jupyter notebook src/analysis.ipynb`
2. Chạy cell thống kê mô tả
3. Chạy cell correlation matrix
4. Chạy cell phân tích churn

---

## 5. HƯỚNG DẪN SQL

### 5.1. Kết nối MySQL

#### Cách 1: Kết nối từ command line
```bash
mysql -u root foodpanda_db
```

**Nếu MySQL yêu cầu password:**
```bash
mysql -u root -p foodpanda_db
# Nhập password khi được hỏi
```

### 5.2. Sử dụng Views

#### 1. `vw_daily_orders` - Tổng hợp đơn hàng theo ngày

**Xem 10 ngày gần nhất:**
```sql
SELECT * FROM vw_daily_orders 
ORDER BY order_date DESC 
LIMIT 10;
```

**Xem tổng doanh thu:**
```sql
SELECT 
    SUM(total_revenue) AS total_revenue_all_time,
    AVG(total_revenue) AS avg_daily_revenue,
    MAX(total_revenue) AS max_daily_revenue
FROM vw_daily_orders;
```

#### 2. `vw_restaurant_stats` - Thống kê theo nhà hàng

**Xem top 10 nhà hàng:**
```sql
SELECT * FROM vw_restaurant_stats 
ORDER BY total_revenue DESC 
LIMIT 10;
```

**Xem nhà hàng có rating cao nhất:**
```sql
SELECT * FROM vw_restaurant_stats 
WHERE avg_rating IS NOT NULL
ORDER BY avg_rating DESC 
LIMIT 10;
```

#### 3. `vw_customer_stats` - Thống kê khách hàng

**Xem top 10 khách hàng chi tiêu nhiều nhất:**
```sql
SELECT * FROM vw_customer_stats 
ORDER BY total_spent DESC 
LIMIT 10;
```

**Phân tích khách hàng churned:**
```sql
SELECT 
    churned,
    COUNT(*) AS customer_count,
    SUM(total_spent) AS total_revenue_lost,
    AVG(total_spent) AS avg_spent
FROM vw_customer_stats
GROUP BY churned;
```

### 5.3. Các queries phân tích hữu ích

#### Thống kê theo thành phố
```sql
SELECT 
    city,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) AS total_revenue,
    AVG(price) AS avg_order_value,
    COUNT(DISTINCT restaurant_name) AS total_restaurants
FROM foodpanda_orders
GROUP BY city
ORDER BY total_revenue DESC;
```

#### Thống kê theo phương thức thanh toán
```sql
SELECT 
    payment_method,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) AS total_revenue,
    AVG(price) AS avg_order_value,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM foodpanda_orders), 2) AS percentage
FROM foodpanda_orders
GROUP BY payment_method
ORDER BY total_revenue DESC;
```

#### Phân tích churn rate
```sql
SELECT 
    churned,
    COUNT(DISTINCT customer_id) AS customer_count,
    ROUND(COUNT(DISTINCT customer_id) * 100.0 / 
          (SELECT COUNT(DISTINCT customer_id) FROM foodpanda_orders), 2) AS percentage
FROM foodpanda_orders
GROUP BY churned;
```

#### Thống kê theo category món ăn
```sql
SELECT 
    category,
    COUNT(*) AS total_items,
    SUM(quantity) AS total_quantity_sold,
    SUM(price) AS total_revenue,
    AVG(price) AS avg_price,
    COUNT(DISTINCT dish_name) AS unique_dishes
FROM foodpanda_orders
WHERE category IS NOT NULL
GROUP BY category
ORDER BY total_revenue DESC;
```

#### Phân tích rating
```sql
SELECT 
    rating,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / 
          (SELECT COUNT(*) FROM foodpanda_orders WHERE rating IS NOT NULL), 2) AS percentage
FROM foodpanda_orders
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating DESC;
```

### 5.4. Các lệnh SQL hữu ích

#### Xem cấu trúc bảng
```sql
DESCRIBE foodpanda_orders;
```

#### Đếm tổng số dòng
```sql
SELECT COUNT(*) FROM foodpanda_orders;
```

#### Xem dữ liệu mẫu
```sql
SELECT * FROM foodpanda_orders LIMIT 10;
```

#### Xem các views đã tạo
```sql
SHOW FULL TABLES WHERE Table_type = 'VIEW';
```

#### Chạy queries từ file
```bash
mysql -u root foodpanda_db < sql/queries.sql
```

---

## 6. BÁO CÁO PHÂN TÍCH

### 6.1. Tổng quan dữ liệu

- **Tổng số dòng:** 6,000 đơn hàng
- **Số cột:** 20 cột
- **Thời gian:** Từ 2023-08 đến 2025-08
- **Số khách hàng:** ~4,533 khách hàng duy nhất
- **Số nhà hàng:** 5 nhà hàng

### 6.2. Phân tích thống kê mô tả

#### Các biến số:
- **Quantity:** Trung bình 2.99, Min: 1, Max: 5
- **Price:** Trung bình 800.52, Min: 100.3, Max: 1499.95
- **Order Frequency:** Trung bình 25.30, Min: 1, Max: 50
- **Loyalty Points:** Trung bình 250.17, Min: 0, Max: 500
- **Rating:** Trung bình 2.99, Min: 1, Max: 5

#### Phân phối dữ liệu:
- Dữ liệu có phân phối **lệch phải (right-skewed)** cho các biến doanh thu
- Skewness cao → cần log-transform nếu sử dụng cho mô hình machine learning

### 6.3. Insights chính

#### 1. Phân phối dữ liệu
- Dữ liệu có phân phối lệch phải → phù hợp với dữ liệu doanh thu thực tế
- Cần log-transform nếu sử dụng cho mô hình machine learning

#### 2. Mối quan hệ giữa các biến
- **Quantity vs Price:** Có mối quan hệ tích cực
- **Order Frequency vs Loyalty Points:** Có mối quan hệ chặt chẽ
- **Rating vs Order Value:** Đơn hàng giá trị cao thường có rating tốt hơn

#### 3. Xu hướng thời gian
- Doanh thu biến động theo ngày/tháng
- Có thể phát hiện patterns theo mùa, ngày trong tuần

#### 4. Delivery Status
- Có sự khác biệt về giá trung bình giữa các trạng thái giao hàng
- Cần cải thiện delivery để tăng customer satisfaction

### 6.4. Recommendations

#### 1. Giảm Churn Rate
- ✅ Tập trung vào khách hàng có order frequency thấp
- ✅ Tạo chương trình khuyến mãi cho khách hàng có nguy cơ churn
- ✅ Cải thiện customer service cho khách hàng Inactive

#### 2. Tăng Doanh Thu
- ✅ Tập trung marketing vào thành phố có tiềm năng cao
- ✅ Khuyến khích khách hàng sử dụng phương thức thanh toán có giá trị đơn hàng cao hơn
- ✅ Tăng giá trị đơn hàng trung bình thông qua upselling

#### 3. Cải thiện Dịch vụ
- ✅ Tập trung vào category và nhà hàng có rating thấp
- ✅ Cải thiện delivery status để tăng customer satisfaction
- ✅ Tối ưu hóa thời gian giao hàng

#### 4. Loyalty Program
- ✅ Tăng giá trị rewards cho khách hàng Platinum
- ✅ Tạo incentives để khách hàng Bronze/Silver nâng cấp tier
- ✅ Personalize offers dựa trên loyalty tier

#### 5. Data-Driven Decisions
- ✅ Sử dụng insights để tối ưu hóa pricing strategy
- ✅ Phát triển mô hình dự báo doanh thu
- ✅ Xây dựng churn prediction model

### 6.5. Kết quả trực quan hóa

#### Biểu đồ đã tạo:
1. **Histogram:** Phân phối giá trị đơn hàng
2. **Boxplot:** So sánh giá theo delivery status
3. **Scatterplot:** Quantity vs Price
4. **Heatmap:** Ma trận tương quan
5. **Time Series:** Doanh thu theo ngày/tháng
6. **Interactive Dashboard:** Tổng hợp nhiều biểu đồ

---

## 7. HƯỚNG DẪN THUYẾT TRÌNH

### 7.1. Cấu trúc thuyết trình (15-20 phút)

#### Slide 1: Tổng quan dự án
- 🎯 Mục tiêu: Mô phỏng quy trình tự động hóa xử lý dữ liệu hóa đơn
- 📊 Nguồn dữ liệu: Foodpanda Order & Delivery Trends (Kaggle)
- 👥 Đội ngũ: 5 thành viên với vai trò chuyên biệt

#### Slide 2: Đội ngũ thực hiện
- Phân công nhiệm vụ rõ ràng theo chuyên môn
- Mỗi thành viên phụ trách một module cụ thể

#### Slide 3: Kiến trúc hệ thống
- Sơ đồ tổng quan: Raw Data → ETL → Database → Analysis → Visualization
- Key Components: ETL Pipeline, Database, Processing, Output

#### Slide 4: Công nghệ sử dụng
- Backend: Python 3.8+, MySQL 8.0+
- Data Processing: Pandas, NumPy
- Visualization: Matplotlib, Seaborn, Plotly

#### Slide 5: Quy trình làm việc
- 8 bước: Collection → Validation → Setup → Import → Cleaning → Analysis → Visualization → Report

#### Slide 6: Database Design
- Bảng chính: `foodpanda_orders` với 20+ columns
- 7 indexes: Tối ưu query performance
- 3 views: Đơn giản hóa queries phức tạp

#### Slide 7: ETL Pipeline
- Extract: Đọc CSV file
- Transform: Convert dates, clean strings, validate
- Load: Import vào MySQL với chunking

#### Slide 8: Data Cleaning
- Xử lý missing values, duplicates, outliers
- Kết quả: Raw data ~6000 dòng → Cleaned data ~4500 dòng

#### Slide 9: Data Analysis
- Thống kê mô tả, phân tích phân phối, tương quan
- Phân tích trends, customer behavior, churn rate

#### Slide 10: Data Visualization
- Static charts: Histogram, Boxplot, Scatter, Heatmap, Time series
- Interactive charts: Plotly với tooltips, zoom/pan

#### Slide 11: Kết quả chính
- Technical: ETL pipeline hoàn chỉnh, database tối ưu
- Business Insights: Top nhà hàng, thành phố, phương thức thanh toán

#### Slide 12: Demo
- Live demonstration: ETL pipeline, Database queries, Visualizations

#### Slide 13: Hạn chế & Thách thức
- Dữ liệu tĩnh, quy mô nhỏ, chưa có API, dashboard web, ML models

#### Slide 14: Hướng phát triển
- Ngắn hạn: API REST, Dashboard web, Unit tests
- Trung hạn: Real-time streaming, ML models, Airflow
- Dài hạn: Data warehouse, Mobile app, Recommendation system

#### Slide 15: Bài học kinh nghiệm
- Technical: Data quality, Database design, Automation, Documentation
- Teamwork: Phân công rõ ràng, Communication, Code review

#### Slide 16: Kết luận
- Thành tựu: Hệ thống hoàn chỉnh, Database tối ưu, Insights có giá trị
- Giá trị: Nền tảng vững chắc, có thể mở rộng

#### Slide 17: Q&A
- Chuẩn bị trả lời các câu hỏi về kiến trúc, công nghệ, kết quả, hướng phát triển

### 7.2. Tips thuyết trình

1. **Thời gian:** 15-20 phút (khoảng 1 phút/slide)
2. **Tone:** Tự tin, nhiệt tình, chuyên nghiệp
3. **Visual:** Sử dụng biểu đồ, sơ đồ, screenshots
4. **Demo:** Chuẩn bị sẵn demo, test trước
5. **Q&A:** Chuẩn bị trả lời các câu hỏi thường gặp

### 7.3. Checklist trước khi thuyết trình

- [ ] Kiểm tra tất cả slides hiển thị đúng
- [ ] Test demo trước
- [ ] Chuẩn bị backup (PDF, video)
- [ ] Kiểm tra thiết bị (projector, microphone)
- [ ] Rehearse ít nhất 2 lần
- [ ] Chuẩn bị nước uống

---

## 8. QUICK REFERENCE

### 8.1. Commands Cheat Sheet

```bash
# Setup
pip install -r requirements.txt
python src/setup_database.py

# Import
python src/import_to_sql.py --validate
python src/import_to_sql.py

# Check
python src/check_database.py

# Notebooks
jupyter notebook src/data_cleaning.ipynb
jupyter notebook src/analysis.ipynb
jupyter notebook src/visualization.ipynb

# SQL
mysql -u root -p foodpanda_db < sql/queries.sql
mysql -u root -p foodpanda_db
```

### 8.2. Cấu trúc dự án

```
foodpanda-analytics/
├── data/              # Dữ liệu (CSV files)
├── src/               # Source code (Python scripts, Notebooks)
├── sql/               # SQL scripts (schema, queries)
├── reports/           # Báo cáo và tài liệu
├── logs/              # Log files
├── README.md          # Tài liệu chính
└── requirements.txt   # Dependencies
```

### 8.3. Database Info

- **Host:** localhost
- **Database:** foodpanda_db
- **Port:** 3306
- **Table:** `foodpanda_orders`
- **Views:** `vw_daily_orders`, `vw_restaurant_stats`, `vw_customer_stats`

### 8.4. Queries mẫu

```sql
-- Xem tổng hợp đơn hàng
SELECT * FROM vw_daily_orders LIMIT 10;

-- Top nhà hàng
SELECT * FROM vw_restaurant_stats LIMIT 10;

-- Top khách hàng
SELECT * FROM vw_customer_stats LIMIT 10;
```

---

## 9. TROUBLESHOOTING

### 9.1. Lỗi kết nối database

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

### 9.2. Lỗi: "Access denied for user 'root'@'localhost'"

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

### 9.3. Lỗi: "ModuleNotFoundError: No module named 'config'"

**Nguyên nhân:**
- Đang chạy script từ thư mục sai
- Virtual environment chưa được activate

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

### 9.4. Lỗi: "File không tồn tại: data/foodpanda_orders.csv"

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

### 9.5. Lỗi: "Table 'foodpanda_orders' already exists"

**Nguyên nhân:**
- Bảng đã tồn tại từ lần chạy trước

**Giải pháp:**
```bash
# Option 1: Replace (xóa và tạo lại)
python src/import_to_sql.py

# Option 2: Append (thêm dữ liệu mới)
python src/import_to_sql.py --append
```

### 9.6. Lỗi: "Jupyter command not found"

**Nguyên nhân:**
- Jupyter chưa được cài đặt

**Giải pháp:**
```bash
pip install jupyter
```

### 9.7. Lỗi import dữ liệu

**Nguyên nhân:**
- File CSV không tồn tại
- Cấu trúc CSV không đúng
- Database chưa được setup

**Giải pháp:**
```bash
# 1. Kiểm tra file CSV
ls -lh data/foodpanda_orders.csv

# 2. Validate dữ liệu
python src/import_to_sql.py --validate

# 3. Setup lại database
python src/setup_database.py
```

### 9.8. Lỗi thiếu packages

**Nguyên nhân:**
- Chưa cài đặt dependencies
- Virtual environment chưa được activate

**Giải pháp:**
```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# 2. Cài đặt lại packages
pip install -r requirements.txt

# 3. Hoặc cài từng package
pip install pandas numpy sqlalchemy pymysql matplotlib seaborn plotly jupyter
```

---

## 📚 TÀI LIỆU THAM KHẢO

- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **MySQL Documentation:** https://dev.mysql.com/doc/
- **Matplotlib Documentation:** https://matplotlib.org/stable/contents.html
- **Seaborn Documentation:** https://seaborn.pydata.org/
- **Plotly Documentation:** https://plotly.com/python/

---

## 📞 LIÊN HỆ

- **Trưởng nhóm:** Nguyễn Thái Bảo (Data Engineer)
- **Repository:** (Cập nhật link nếu có)
- **Email:** (Cập nhật nếu có)

---

**Tài liệu này được tạo bởi Người 5 - Report & Documentation**  
**Ngày cập nhật:** 2025-01-27  
**Phiên bản:** 1.0

**Chúc bạn sử dụng dự án thành công! 🎉**


