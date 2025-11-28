# Foodpanda Order Data Pipeline — Báo cáo dự án

## 1. Tiêu đề & Giới thiệu

**Tiêu đề:** Foodpanda Order Data Pipeline — Báo cáo dự án

**Giới thiệu:**

Dự án này được xây dựng nhằm mục đích thiết kế và triển khai một pipeline dữ liệu (Data Pipeline) hoàn chỉnh để xử lý dữ liệu đơn hàng của Foodpanda. Mục tiêu chính là chuyển đổi dữ liệu thô từ file CSV, làm sạch, chuẩn hóa và lưu trữ vào hệ quản trị cơ sở dữ liệu MySQL để phục vụ cho việc phân tích và báo cáo.

**Ý nghĩa:**
Việc xây dựng pipeline này giúp tự động hóa quy trình xử lý dữ liệu, đảm bảo tính nhất quán và độ tin cậy của dữ liệu. Nó tạo nền tảng vững chắc cho các hoạt động Business Intelligence (BI), giúp doanh nghiệp đưa ra các quyết định dựa trên dữ liệu (Data-Driven Decisions) như tối ưu hóa thực đơn, chiến lược giá và chăm sóc khách hàng.

**Bối cảnh:**
Đây là một dự án mô phỏng thực tế kết hợp giữa Data Engineering và Data Analysis, tái hiện quy trình làm việc chuyên nghiệp từ khâu Ingestion (thu thập) đến Visualization (trực quan hóa).

---

## 2. Mô tả cấu trúc dự án

Cấu trúc dự án được tổ chức theo tiêu chuẩn Data Engineering để đảm bảo tính rõ ràng, dễ bảo trì và mở rộng:

- **`data/`**: Chứa dữ liệu thô (`foodpanda_orders.csv`) và dữ liệu đã qua xử lý. Đây là nơi lưu trữ đầu vào của pipeline.
- **`src/`**: Chứa mã nguồn chính của dự án.
    - `import_to_sql.py`: Script chính thực hiện ETL (Extract, Transform, Load).
    - `config.py`: Quản lý các cấu hình như thông tin database, đường dẫn file, tên cột.
    - `check_environment.py`, `check_database.py`: Các script tiện ích để kiểm tra môi trường.
    - Notebooks (`analysis.ipynb`, `data_cleaning.ipynb`, `visualization.ipynb`): Dùng cho việc phân tích khám phá (EDA) và trực quan hóa.
- **`sql/`**: Chứa các file SQL định nghĩa cấu trúc database.
    - `schema.sql`: Script tạo bảng và các Views.
    - `queries.sql`: Các câu truy vấn mẫu.
- **`logs/`**: Lưu trữ các file log (`import.log`) ghi lại quá trình chạy của pipeline, giúp theo dõi và debug lỗi.
- **`reports/`**: Chứa báo cáo cuối cùng của dự án (file này).

**Tại sao cấu trúc này phù hợp?**
Việc tách biệt mã nguồn (`src`), dữ liệu (`data`), và định nghĩa cơ sở dữ liệu (`sql`) giúp dự án dễ quản lý phiên bản (git), dễ triển khai (deployment) và cho phép các thành viên trong nhóm (Engineer, Analyst) làm việc độc lập mà không gây xung đột.

---

## 3. Mô tả Pipeline (ETL Workflow)

Quy trình ETL được thực hiện chủ yếu qua script `src/import_to_sql.py` và `sql/schema.sql`.

### Sơ đồ luồng dữ liệu:
`CSV (Raw Data)` -> **Ingestion** (Pandas) -> **Validation** -> **Cleaning** -> **Load** (MySQL) -> **Storage** (Tables & Views) -> **Analysis**

### Chi tiết từng bước:

1.  **Ingestion (`src/import_to_sql.py`)**:
    - Script đọc file CSV sử dụng thư viện `pandas` với tùy chọn `low_memory=False` để xử lý file lớn hiệu quả hơn.
    - Sử dụng `chunksize` khi import vào database để tránh quá tải bộ nhớ.

2.  **Validation**:
    - Kiểm tra sự tồn tại của file nguồn.
    - Kiểm tra cấu trúc cột: Đảm bảo file CSV có đủ các cột mong đợi (`EXPECTED_COLUMNS` trong `config.py`).
    - Kiểm tra dữ liệu: Phát hiện các giá trị thiếu (missing values), dòng trùng lặp và cảnh báo qua log.

3.  **Cleaning**:
    - **Chuẩn hóa Text**: Loại bỏ khoảng trắng thừa ở đầu/cuối chuỗi (`strip()`), xử lý giá trị `nan`.
    - **Chuẩn hóa Số**: Chuyển đổi các cột số (`quantity`, `price`, `rating`, v.v.) về đúng kiểu dữ liệu, xử lý lỗi chuyển đổi (`errors='coerce'`).
    - **Chuẩn hóa Ngày tháng**: Chuyển đổi các cột ngày (`order_date`, `signup_date`, v.v.) sang định dạng `datetime` chuẩn của SQL.

4.  **Load**:
    - Sử dụng `sqlalchemy` để kết nối và đẩy dữ liệu vào MySQL.
    - Hỗ trợ hai chế độ: `replace` (ghi đè bảng cũ) hoặc `append` (thêm vào bảng hiện có).
    - Sử dụng transaction để đảm bảo tính toàn vẹn dữ liệu.

5.  **Logging & Error Handling**:
    - Hệ thống logging ghi lại chi tiết từng bước (Info), các cảnh báo về dữ liệu (Warning) và lỗi nghiêm trọng (Error) vào cả file log và màn hình console.
    - `try-except` blocks được sử dụng để bắt lỗi kết nối database hoặc lỗi đọc file, đảm bảo chương trình dừng một cách an toàn (graceful exit).

### Storage (`sql/schema.sql`):

-   **Bảng `foodpanda_orders`**: Được thiết kế với các kiểu dữ liệu tối ưu (VARCHAR, INT, DECIMAL, DATE) và có các **Index** (`idx_customer_id`, `idx_order_date`, v.v.) để tăng tốc độ truy vấn.

-   **Views (Tối ưu phân tích)**:
    -   `vw_daily_orders`: Tổng hợp doanh thu, số đơn hàng theo ngày. Giúp Analyst nhanh chóng vẽ biểu đồ xu hướng mà không cần query bảng gốc lớn.
    -   `vw_restaurant_stats`: Thống kê hiệu suất từng nhà hàng (số đơn, doanh thu, rating trung bình).
    -   `vw_customer_stats`: Tổng hợp hành vi khách hàng (tổng chi tiêu, tần suất), hỗ trợ phân khúc khách hàng.

### Analysis & Visualization:
-   `data_cleaning.ipynb`: Ghi lại quá trình khám phá và thử nghiệm logic làm sạch dữ liệu.
-   `analysis.ipynb`: Chứa các phân tích sâu về xu hướng và hành vi.
-   `visualization.ipynb`: Tạo các biểu đồ trực quan.

---

## 4. Insight chính

Dựa trên phân tích dữ liệu từ hệ thống, dưới đây là các insight quan trọng:

| Metric | Giá trị / Kết quả | Ghi chú |
| :--- | :--- | :--- |
| **Ngày đặt hàng cao nhất** | **2024-09-08** | 20 đơn hàng trong ngày |
| **Nhà hàng doanh thu cao nhất** | **Subway** | Tổng doanh thu: ~1,009,983 |
| **Khách hàng thân thiết nhất** | **C6466** | Tần suất đặt hàng (Frequency Stat): 50 |
| **Doanh thu trung bình ngày** | **~6,580** | Mức trung bình ổn định |

**Mối tương quan (Correlation Analysis):**
Phân tích tương quan giữa các chỉ số chính cho thấy:
-   **Giá (Price) vs Số lượng (Quantity)**: Tương quan rất thấp (~ -0.007). Điều này cho thấy giá trị đơn hàng không phụ thuộc tuyến tính vào số lượng món (có thể do sự chênh lệch giá lớn giữa các món ăn).
-   **Giá vs Rating**: Không có tương quan rõ ràng. Giá cao không đảm bảo rating cao và ngược lại.
-   **Lưu ý**: Dữ liệu hiện tại thiếu các cột *Phí giao hàng (Delivery Fee)* và *Thời gian chuẩn bị (Prep Time)* nên không thể phân tích tương quan của các yếu tố này với Tổng hóa đơn như yêu cầu ban đầu.

---

## 5. Vai trò trong nhóm (Group Roles)

1.  **Data Engineer**:
    -   **Trách nhiệm**: Thiết kế kiến trúc pipeline, viết script `import_to_sql.py`, thiết kế schema SQL (`schema.sql`), cấu hình kết nối database.
    -   **Output**: Pipeline hoạt động ổn định, dữ liệu được lưu trữ an toàn và có cấu trúc trong MySQL.

2.  **Data Cleaning Specialist**:
    -   **Trách nhiệm**: Phân tích chất lượng dữ liệu thô, định nghĩa các quy tắc làm sạch (xử lý null, chuẩn hóa định dạng), viết logic cho hàm `clean_dataframe`.
    -   **Output**: Dữ liệu sạch, nhất quán, sẵn sàng cho phân tích.

3.  **Analyst**:
    -   **Trách nhiệm**: Viết các câu truy vấn SQL, tạo Views, thực hiện phân tích thống kê để tìm ra các insight (như top nhà hàng, xu hướng ngày).
    -   **Output**: Các bảng số liệu thống kê, các insight kinh doanh giá trị.

4.  **Visualization Specialist**:
    -   **Trách nhiệm**: Sử dụng Python (Matplotlib/Seaborn) hoặc công cụ BI để biến số liệu thành biểu đồ trực quan, dễ hiểu.
    -   **Output**: Các biểu đồ xu hướng, biểu đồ tròn, heatmap thể hiện tương quan.

5.  **Reporter**:
    -   **Trách nhiệm**: Tổng hợp tất cả kết quả từ các thành viên, viết báo cáo cuối cùng, đảm bảo văn phong chuyên nghiệp và cấu trúc logic.
    -   **Output**: File báo cáo dự án hoàn chỉnh (`reports/Foodpanda_Order_Data_Pipeline_Report.md`).

---

## 6. Đánh giá chất lượng mã

-   **Tính rõ ràng**: Mã nguồn được tổ chức tốt, tên hàm và biến gợi nhớ (self-explanatory). Docstrings đầy đủ cho từng hàm giúp dễ dàng hiểu mục đích sử dụng.
-   **Logging**: Hệ thống logging được triển khai bài bản, ghi log ra cả file và console với định dạng chuẩn (timestamp, level, message). Điều này rất quan trọng cho việc vận hành thực tế.
-   **Error Handling**: Các khối `try-except` bao quát các lỗi phổ biến (File Not Found, DB Connection Error). Tuy nhiên, có thể cải thiện thêm việc xử lý lỗi chi tiết cho từng dòng dữ liệu (row-level error handling) thay vì fail cả batch nếu có lỗi nghiêm trọng.
-   **Tối ưu hóa Schema SQL**: Việc sử dụng đúng kiểu dữ liệu và đánh Index cho các cột hay truy vấn (`customer_id`, `order_date`) cho thấy tư duy tối ưu hóa tốt. Các Views giúp giảm tải cho việc viết query lặp lại.
-   **Khả năng mở rộng**: Việc sử dụng `chunksize` khi import cho phép pipeline xử lý các file CSV lớn hơn bộ nhớ RAM. Cấu trúc module hóa (`config.py` tách riêng) giúp dễ dàng thay đổi cấu hình môi trường.

---

## 7. Kết luận & Đề xuất cải tiến

**Tóm tắt:**
Dự án đã xây dựng thành công một pipeline xử lý dữ liệu đơn hàng Foodpanda từ file CSV thô vào cơ sở dữ liệu MySQL. Hệ thống đảm bảo các tiêu chuẩn cơ bản của Data Engineering về cấu trúc, làm sạch dữ liệu và logging. Các insight rút ra từ dữ liệu cung cấp cái nhìn tổng quan về hoạt động kinh doanh.

**Điểm mạnh:**
-   Cấu trúc dự án chuẩn mực, dễ bảo trì.
-   Pipeline có khả năng xử lý file lớn (chunking).
-   Hệ thống logging và validation tốt.

**Đề xuất cải tiến:**
Để nâng cấp hệ thống lên mức production-ready và chuyên nghiệp hơn, nhóm đề xuất:
1.  **Tự động hóa với Airflow**: Chuyển script Python thành các DAGs trong Apache Airflow để lên lịch chạy tự động hàng ngày (daily batch) và quản lý phụ thuộc tốt hơn.
2.  **Containerization (Docker)**: Đóng gói toàn bộ ứng dụng (Python env, MySQL) vào Docker containers để đảm bảo môi trường chạy nhất quán trên mọi máy (tránh lỗi "works on my machine").
3.  **Transformation với dbt**: Sử dụng dbt (data build tool) để quản lý các biến đổi SQL (Views, Tables) thay vì viết SQL thuần trong script hoặc schema file. Điều này giúp quản lý lineage và test dữ liệu tốt hơn.
4.  **Dashboard hóa**: Kết nối database với các công cụ BI open-source như **Apache Superset** hoặc **Metabase** để xây dựng dashboard tương tác realtime thay vì các báo cáo tĩnh.
