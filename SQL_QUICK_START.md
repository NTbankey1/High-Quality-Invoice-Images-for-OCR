# SQL QUICK START
## Hướng dẫn nhanh để chạy SQL

---

## 🔌 KẾT NỐI

```bash
mysql -u root foodpanda_db
```

---

## 📊 5 LỆNH CƠ BẢN NHẤT

### 1. Xem các bảng
```sql
SHOW TABLES;
```

### 2. Xem top 10 nhà hàng
```sql
SELECT * FROM vw_restaurant_stats LIMIT 10;
```

### 3. Xem top 10 khách hàng
```sql
SELECT * FROM vw_customer_stats LIMIT 10;
```

### 4. Xem đơn hàng theo ngày
```sql
SELECT * FROM vw_daily_orders LIMIT 10;
```

### 5. Thống kê theo thành phố
```sql
SELECT city, COUNT(*) as orders, SUM(price) as revenue 
FROM foodpanda_orders 
GROUP BY city 
ORDER BY revenue DESC 
LIMIT 10;
```

---

## 🚀 CHẠY TẤT CẢ QUERIES

```bash
mysql -u root foodpanda_db < sql/queries.sql
```

---

## 📝 THOÁT

```sql
EXIT;
```

---

**Xem chi tiết:** `reports/HUONG_DAN_SQL.md`

