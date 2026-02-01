# KỊCH BẢN TEST - HỆ THỐNG ODOO TÍCH HỢP

## Mục tiêu
Kiểm tra tính năng **TÍCH HỢP HỆ THỐNG (Mức 1)** và **TỰ ĐỘNG HÓA QUY TRÌNH (Mức 2)** của các module Odoo đã phát triển.

---

## 📋 DANH SÁCH MODULE CẦN TEST

1. **Nhân sự** (`nhan_su`) - Module gốc
2. **Quản lý văn bản** (`quan_ly_van_ban`)
3. **Quản lý tài sản cá nhân** (`quan_ly_tai_san`)
4. **Tài sản doanh nghiệp** (`tai_san_doanh_nghiep`)
5. **Tài chính kế toán** (`tai_chinh_ke_toan`) - Module tích hợp chính

---

## 🔧 CHUẨN BỊ

### Bước 1: Khởi động hệ thống
```bash
cd /home/nghiax/odoo
./odoo-bin -c odoo.conf
```

### Bước 2: Truy cập hệ thống
- URL: http://localhost:8069
- Bật Developer Mode: Thêm `?debug=1` vào URL

### Bước 3: Cài đặt tất cả module
1. Vào **Apps**
2. Click **Update Apps List**
3. Tìm và cài đặt theo thứ tự:
   - ✅ Nhân sự
   - ✅ Tài sản doanh nghiệp
   - ✅ Quản lý văn bản
   - ✅ Quản lý tài sản cá nhân
   - ✅ Tài chính kế toán (cài cuối cùng)

---

# PHẦN 1: TEST TÍCH HỢP HỆ THỐNG (MỨC 1)

## ✅ Test Case 1.1: Chia sẻ chung Database

**Mục tiêu:** Kiểm tra tất cả module sử dụng chung một database, không có database riêng biệt

### Bước thực hiện:
1. Mở terminal và kết nối database:
```bash
wsl bash -c "PGPASSWORD=odoo psql -h localhost -p 5431 -U odoo -d odoo"
```

2. Liệt kê tất cả các bảng:
```sql
\dt
```

3. Kiểm tra các bảng từ các module:
```sql
-- Kiểm tra bảng nhân viên
SELECT * FROM nhan_vien LIMIT 1;

-- Kiểm tra bảng tài sản
SELECT * FROM tai_san LIMIT 1;

-- Kiểm tra bảng lương (tích hợp)
SELECT * FROM bang_luong LIMIT 1;

-- Kiểm tra bảng chi phí (tích hợp)
SELECT * FROM chi_phi LIMIT 1;
```

### Kết quả mong đợi:
✅ Tất cả các bảng đều nằm trong cùng một database `odoo`  
✅ Không có database riêng cho từng module  
✅ Các bảng có thể truy vấn được

---

## ✅ Test Case 1.2: Nhân sự là dữ liệu gốc - Đồng bộ sang Bảng lương

**Mục tiêu:** Kiểm tra dữ liệu nhân viên là nguồn gốc và được đồng bộ tự động

### Bước thực hiện:

#### 1. Tạo nhân viên mới
1. Vào menu **Nhân sự → Nhân viên**
2. Click **Create**
3. Nhập thông tin:
   - Mã định danh: `NV001`
   - Họ và tên: `Nguyễn Văn A`
   - Ngày sinh: `01/01/1990`
   - Email: `nva@company.com`
   - Số điện thoại: `0912345678`
   - Quê quán: `Hà Nội`
4. Click **Save**

#### 2. Kiểm tra tự động tạo bảng lương (MỨC 2)
1. Vào menu **Tài chính kế toán → Quản lý lương**
2. Tìm bảng lương của `Nguyễn Văn A`

### Kết quả mong đợi:
✅ **MỨC 1**: Nhân viên được tạo thành công  
✅ **MỨC 2**: Hệ thống **TỰ ĐỘNG** tạo bảng lương tháng hiện tại cho nhân viên mới  
✅ Họ tên và email được đồng bộ tự động từ nhân viên  
✅ Lương cơ bản có giá trị mặc định (5,000,000)  
✅ Ghi chú: "Bảng lương tự động tạo cho nhân viên mới"

### Kiểm tra database:
```sql
-- Kiểm tra nhân viên vừa tạo
SELECT * FROM nhan_vien WHERE ho_va_ten = 'Nguyễn Văn A';

-- Kiểm tra bảng lương tự động tạo
SELECT bl.*, nv.ho_va_ten 
FROM bang_luong bl 
JOIN nhan_vien nv ON bl.nhan_vien_id = nv.id 
WHERE nv.ho_va_ten = 'Nguyễn Văn A';
```

---

## ✅ Test Case 1.3: Tích hợp Nhân sự - Chi phí

**Mục tiêu:** Kiểm tra chi phí nhân sự sử dụng dữ liệu từ module Nhân sự

### Bước thực hiện:

#### 1. Tạo chi phí nhân sự
1. Vào menu **Tài chính kế toán → Chi phí**
2. Click **Create**
3. Nhập thông tin:
   - Tên chi phí: `Đào tạo nhân viên`
   - Loại chi phí: `Chi phí nhân sự`
   - Nhân viên liên quan: Chọn `Nguyễn Văn A` (từ dropdown)
   - Số tiền: `3,000,000`
   - Ngày chi: Hôm nay
   - Mô tả: `Khóa học nâng cao kỹ năng`
4. Click **Save**

#### 2. Kiểm tra đồng bộ dữ liệu
1. Xem trường "Họ tên" tự động hiển thị
2. Kiểm tra dữ liệu nhân viên không bị trùng lặp

### Kết quả mong đợi:
✅ **MỨC 1**: Dropdown nhân viên lấy từ module `nhan_su`  
✅ Họ tên được đồng bộ tự động (read-only)  
✅ Không cần nhập lại thông tin nhân viên  
✅ Dữ liệu nhất quán giữa 2 module

### Kiểm tra database:
```sql
-- Kiểm tra chi phí có liên kết với nhân viên
SELECT cp.*, nv.ho_va_ten, nv.email 
FROM chi_phi cp 
JOIN nhan_vien nv ON cp.nhan_vien_id = nv.id 
WHERE cp.loai_chi_phi = 'nhan_su';
```

---

## ✅ Test Case 1.4: Tích hợp Tài sản - Chi phí

**Mục tiêu:** Kiểm tra chi phí tài sản liên kết với module Tài sản doanh nghiệp

### Bước thực hiện:

#### 1. Tạo tài sản
1. Vào menu **Tài sản doanh nghiệp → Tài sản**
2. Click **Create**
3. Nhập thông tin:
   - Mã tài sản: `TS001`
   - Tên tài sản: `Máy tính Dell Latitude`
   - Loại tài sản: `Thiết bị`
   - Giá trị: `20,000,000`
   - Tình trạng: `Mới`
   - Vị trí: `Phòng IT`
4. Click **Save**

#### 2. Tạo chi phí tài sản
1. Vào menu **Tài chính kế toán → Chi phí**
2. Click **Create**
3. Nhập thông tin:
   - Tên chi phí: `Sửa chữa máy tính`
   - Loại chi phí: `Chi phí tài sản`
   - Tài sản liên quan: Chọn `Máy tính Dell Latitude`
   - Số tiền: `1,500,000`
   - Ngày chi: Hôm nay
4. Click **Save**

### Kết quả mong đợi:
✅ **MỨC 1**: Dropdown tài sản lấy từ module `tai_san_doanh_nghiep`  
✅ Tên tài sản được đồng bộ tự động  
✅ Không nhập trùng dữ liệu tài sản  
✅ Liên kết chặt chẽ giữa tài sản và chi phí

### Kiểm tra database:
```sql
-- Kiểm tra chi phí tài sản
SELECT cp.*, ts.ten_tai_san, ts.ma_tai_san 
FROM chi_phi cp 
JOIN tai_san ts ON cp.tai_san_id = ts.id 
WHERE cp.loai_chi_phi = 'tai_san';
```

---

## ✅ Test Case 1.5: Không có dữ liệu trùng lặp

**Mục tiêu:** Đảm bảo không nhập liệu trùng lặp, dữ liệu được chia sẻ

### Bước thực hiện:

#### 1. Kiểm tra thông tin nhân viên trên nhiều module
1. Xem thông tin `Nguyễn Văn A` trong module **Nhân sự**
2. Xem thông tin `Nguyễn Văn A` trong **Bảng lương**
3. Xem thông tin `Nguyễn Văn A` trong **Chi phí nhân sự**
4. Xem thông tin `Nguyễn Văn A` trong **Thu chi**

#### 2. Thay đổi thông tin nhân viên
1. Vào **Nhân sự → Nhân viên**
2. Mở record `Nguyễn Văn A`
3. Sửa Email thành: `nguyenvana.new@company.com`
4. Click **Save**

#### 3. Kiểm tra đồng bộ
1. Vào **Tài chính kế toán → Quản lý lương**
2. Mở bảng lương của `Nguyễn Văn A`
3. Kiểm tra Email đã tự động cập nhật chưa

### Kết quả mong đợi:
✅ **MỨC 1**: Email tự động cập nhật ở tất cả các nơi sử dụng  
✅ Chỉ cần sửa 1 lần ở module gốc (Nhân sự)  
✅ Không cần sửa ở từng module riêng  
✅ Dữ liệu luôn nhất quán

### Kiểm tra database:
```sql
-- Kiểm tra email đã cập nhật
SELECT ho_va_ten, email FROM nhan_vien WHERE ho_va_ten = 'Nguyễn Văn A';

-- Kiểm tra bảng lương có email mới
SELECT bl.*, nv.email 
FROM bang_luong bl 
JOIN nhan_vien nv ON bl.nhan_vien_id = nv.id 
WHERE nv.ho_va_ten = 'Nguyễn Văn A';
```

---

# PHẦN 2: TEST TỰ ĐỘNG HÓA QUY TRÌNH (MỨC 2)

## 🤖 Test Case 2.1: Thanh toán lương → Tự động tạo Phiếu chi

**Mục tiêu:** Khi bảng lương được thanh toán, hệ thống tự động tạo phiếu chi

### Bước thực hiện:

#### 1. Chuẩn bị bảng lương
1. Vào **Tài chính kế toán → Quản lý lương**
2. Mở bảng lương của `Nguyễn Văn A`
3. Cập nhật thông tin:
   - Lương cơ bản: `10,000,000`
   - Phụ cấp: `2,000,000`
   - Thưởng: `1,000,000`
   - Bảo hiểm: `1,000,000`
   - Thuế: `500,000`
4. Kiểm tra **Tổng lương**: Phải là `11,500,000`
5. **CHƯA** chuyển trạng thái, click **Save**

#### 2. Đếm số phiếu chi hiện tại
1. Vào **Tài chính kế toán → Thu chi**
2. Đếm tổng số phiếu chi (ghi lại số lượng)

#### 3. Thực hiện thanh toán lương
1. Quay lại bảng lương của `Nguyễn Văn A`
2. Chọn **Ngày thanh toán**: Hôm nay
3. Chuyển **Trạng thái** sang: `Đã thanh toán`
4. Click **Save**

#### 4. Kiểm tra tự động tạo phiếu chi
1. Vào **Tài chính kế toán → Thu chi**
2. Tìm phiếu chi mới nhất

### Kết quả mong đợi:
✅ **MỨC 2 - TỰ ĐỘNG**: Hệ thống TỰ ĐỘNG tạo 1 phiếu chi mới  
✅ Loại phiếu: `Phiếu chi`  
✅ Nội dung: `Chi lương tháng [tháng]/[năm] - Nguyễn Văn A`  
✅ Số tiền: `11,500,000` (đúng với tổng lương)  
✅ Ngày: Trùng với ngày thanh toán  
✅ Người nộp/nhận: `Nguyễn Văn A`  
✅ Trạng thái: `Xác nhận`  
✅ Ghi chú: "Phiếu chi tự động từ bảng lương [id]"  

### Kiểm tra database:
```sql
-- Kiểm tra phiếu chi tự động tạo
SELECT * FROM thu_chi 
WHERE noi_dung LIKE '%Chi lương%Nguyễn Văn A%' 
ORDER BY create_date DESC LIMIT 1;

-- Kiểm tra số tiền khớp với bảng lương
SELECT bl.tong_luong, tc.so_tien 
FROM bang_luong bl 
LEFT JOIN thu_chi tc ON tc.noi_dung LIKE CONCAT('%', bl.id, '%') 
WHERE bl.nhan_vien_id = (SELECT id FROM nhan_vien WHERE ho_va_ten = 'Nguyễn Văn A');
```

### Screenshot cần chụp:
- 📸 Trước khi thanh toán: Danh sách phiếu chi
- 📸 Sau khi thanh toán: Phiếu chi mới được tạo tự động
- 📸 Chi tiết phiếu chi tự động

---

## 🤖 Test Case 2.2: Duyệt chi phí → Tự động tạo Phiếu chi

**Mục tiêu:** Khi chi phí được duyệt, hệ thống tự động tạo phiếu chi

### Bước thực hiện:

#### 1. Tạo chi phí mới
1. Vào **Tài chính kế toán → Chi phí**
2. Click **Create**
3. Nhập thông tin:
   - Tên chi phí: `Mua văn phòng phẩm`
   - Loại chi phí: `Chi phí văn phòng`
   - Số tiền: `5,000,000`
   - Ngày chi: Hôm nay
   - Người duyệt: Chọn nhân viên bất kỳ
4. Giữ **Trạng thái**: `Chờ duyệt`
5. Click **Save**
6. Ghi lại **Mã chi phí** (vd: CP20260201101530)

#### 2. Đếm số phiếu chi hiện tại
1. Vào **Tài chính kế toán → Thu chi**
2. Đếm tổng số phiếu chi
3. Tìm xem đã có phiếu nào với mã chi phí này chưa

#### 3. Duyệt chi phí
1. Quay lại chi phí `Mua văn phòng phẩm`
2. Chuyển **Trạng thái** sang: `Đã duyệt`
3. Click **Save**

#### 4. Kiểm tra phiếu chi tự động
1. Vào **Tài chính kế toán → Thu chi**
2. Tìm phiếu chi mới

### Kết quả mong đợi:
✅ **MỨC 2 - TỰ ĐỘNG**: Hệ thống TỰ ĐỘNG tạo phiếu chi  
✅ Loại phiếu: `Phiếu chi`  
✅ Nội dung: `Chi phí [mã] - Mua văn phòng phẩm`  
✅ Số tiền: `5,000,000`  
✅ Ngày: Trùng với ngày chi  
✅ Trạng thái: `Xác nhận`  
✅ Ghi chú: "Phiếu chi tự động từ chi phí [mã]"  

### Kiểm tra database:
```sql
-- Kiểm tra phiếu chi tự động
SELECT tc.*, cp.ma_chi_phi, cp.ten_chi_phi 
FROM thu_chi tc 
JOIN chi_phi cp ON tc.noi_dung LIKE CONCAT('%', cp.ma_chi_phi, '%') 
WHERE cp.ten_chi_phi = 'Mua văn phòng phẩm';
```

### Screenshot cần chụp:
- 📸 Chi phí ở trạng thái "Chờ duyệt"
- 📸 Sau khi duyệt, phiếu chi tự động xuất hiện
- 📸 Chi tiết phiếu chi khớp với chi phí

---

## 🤖 Test Case 2.3: Bảo trì tài sản → Tự động tạo Chi phí

**Mục tiêu:** Khi tạo phiếu bảo trì tài sản, tự động tạo chi phí tài sản

### Bước thực hiện:

#### 1. Kiểm tra tài sản hiện có
1. Vào **Tài sản doanh nghiệp → Tài sản**
2. Mở tài sản `Máy tính Dell Latitude`

#### 2. Đếm số chi phí hiện tại
1. Vào **Tài chính kế toán → Chi phí**
2. Filter loại: `Chi phí tài sản`
3. Đếm số lượng

#### 3. Tạo phiếu bảo trì
1. Vào **Tài sản doanh nghiệp → Tài sản**
2. Mở `Máy tính Dell Latitude`
3. Vào tab **Bảo trì sửa chữa**
4. Click **Add a line**
5. Nhập (nếu có các trường này):
   - Ngày bảo trì: Hôm nay
   - Chi phí: `2,000,000`
   - Mô tả: `Thay ổ cứng`
6. Click **Save**

#### 4. Kiểm tra chi phí tự động
1. Vào **Tài chính kế toán → Chi phí**
2. Filter loại: `Chi phí tài sản`
3. Tìm chi phí mới

### Kết quả mong đợi:
✅ **MỨC 2 - TỰ ĐỘNG**: Hệ thống TỰ ĐỘNG tạo chi phí  
✅ Tên chi phí: `Bảo trì/Sửa chữa - Máy tính Dell Latitude`  
✅ Loại: `Chi phí tài sản`  
✅ Tài sản liên quan: `Máy tính Dell Latitude`  
✅ Số tiền: `2,000,000`  
✅ Trạng thái: `Chờ duyệt`  
✅ Mô tả: "Chi phí tự động từ bảo trì tài sản"  

### Kiểm tra database:
```sql
-- Kiểm tra chi phí tự động từ bảo trì
SELECT cp.*, ts.ten_tai_san 
FROM chi_phi cp 
JOIN tai_san ts ON cp.tai_san_id = ts.id 
WHERE ts.ten_tai_san = 'Máy tính Dell Latitude' 
AND cp.mo_ta LIKE '%tự động%';
```

---

## 🤖 Test Case 2.4: Trả tài sản hỏng → Tự động tạo Chi phí bồi thường

**Mục tiêu:** Khi trả tài sản với tình trạng hỏng/mất, tự động tạo chi phí bồi thường

### Bước thực hiện:

#### 1. Tạo phiếu mượn tài sản
1. Vào **Tài sản doanh nghiệp → Tài sản**
2. Mở `Máy tính Dell Latitude`
3. Vào tab **Quản lý mượn trả**
4. Click **Add a line**
5. Nhập:
   - Người mượn: Chọn `Nguyễn Văn A`
   - Ngày mượn dự kiến: Hôm nay
   - Ngày trả dự kiến: 7 ngày sau
   - Trạng thái: `Đang mượn`
6. Click **Save**

#### 2. Đếm chi phí hiện tại
1. Vào **Tài chính kế toán → Chi phí**
2. Đếm số chi phí liên quan đến `Nguyễn Văn A`

#### 3. Cập nhật trả tài sản hỏng
1. Quay lại phiếu mượn vừa tạo
2. Cập nhật:
   - **Tình trạng khi trả**: `Hỏng`
   - **Phí bồi thường**: `5,000,000`
   - Ngày trả thực tế: Hôm nay
3. Click **Save**

#### 4. Kiểm tra chi phí bồi thường
1. Vào **Tài chính kế toán → Chi phí**
2. Tìm chi phí mới

### Kết quả mong đợi:
✅ **MỨC 2 - TỰ ĐỘNG**: Hệ thống TỰ ĐỘNG tạo chi phí bồi thường  
✅ Tên: `Bồi thường tài sản hong - Máy tính Dell Latitude`  
✅ Loại: `Chi phí tài sản`  
✅ Nhân viên: `Nguyễn Văn A`  
✅ Tài sản: `Máy tính Dell Latitude`  
✅ Số tiền: `5,000,000`  
✅ Trạng thái: `Chờ duyệt`  
✅ Mô tả: "Chi phí bồi thường tự động - Tài sản hong khi trả"  

### Kiểm tra database:
```sql
-- Kiểm tra chi phí bồi thường
SELECT cp.*, nv.ho_va_ten, ts.ten_tai_san 
FROM chi_phi cp 
JOIN nhan_vien nv ON cp.nhan_vien_id = nv.id 
JOIN tai_san ts ON cp.tai_san_id = ts.id 
WHERE cp.ten_chi_phi LIKE '%Bồi thường%';
```

### Screenshot cần chụp:
- 📸 Phiếu mượn trước khi trả
- 📸 Cập nhật tình trạng hỏng và phí bồi thường
- 📸 Chi phí bồi thường tự động được tạo

---

## 🤖 Test Case 2.5: Xác nhận phiếu thu/chi → Cập nhật Báo cáo

**Mục tiêu:** Khi xác nhận phiếu thu/chi, báo cáo tài chính tự động cập nhật

### Bước thực hiện:

#### 1. Tạo báo cáo tài chính
1. Vào **Tài chính kế toán → Báo cáo tài chính**
2. Click **Create**
3. Nhập:
   - Tên báo cáo: `Báo cáo test tự động`
   - Loại: `Báo cáo tháng`
   - Từ ngày: Đầu tháng này
   - Đến ngày: Cuối tháng này
4. Click **Save**
5. Ghi lại các số liệu:
   - Tổng thu: ?
   - Tổng chi lương: ?
   - Tổng chi phí: ?
   - Lãi/Lỗ: ?

#### 2. Tạo phiếu thu mới
1. Vào **Tài chính kế toán → Thu chi**
2. Click **Create**
3. Nhập:
   - Loại phiếu: `Phiếu thu`
   - Nội dung: `Thu tiền dịch vụ`
   - Số tiền: `10,000,000`
   - Ngày: Hôm nay (trong khoảng báo cáo)
   - Trạng thái: `Nháp`
4. Click **Save**

#### 3. Xác nhận phiếu thu
1. Chuyển **Trạng thái** sang: `Xác nhận`
2. Click **Save**

#### 4. Kiểm tra báo cáo tự động cập nhật
1. Vào **Tài chính kế toán → Báo cáo tài chính**
2. Mở `Báo cáo test tự động`
3. Kiểm tra số liệu

### Kết quả mong đợi:
✅ **MỨC 2 - TỰ ĐỘNG**: Báo cáo TỰ ĐỘNG cập nhật  
✅ Tổng thu tăng thêm: `10,000,000`  
✅ Lãi/Lỗ thay đổi tương ứng  
✅ Không cần click nút "Tính lại" hay "Refresh"  
✅ Real-time update  

### Kiểm tra bằng cách khác:
1. Tạo thêm phiếu chi `5,000,000` và xác nhận
2. Kiểm tra báo cáo có cập nhật ngay không

### Kiểm tra database:
```sql
-- Xem báo cáo có cập nhật không
SELECT * FROM bao_cao_tai_chinh 
WHERE ten_bao_cao = 'Báo cáo test tự động';

-- Xem các phiếu thu/chi trong khoảng thời gian
SELECT * FROM thu_chi 
WHERE ngay >= '2026-02-01' AND ngay <= '2026-02-28' 
AND trang_thai = 'xac_nhan';
```

---

## 🤖 Test Case 2.6: Luồng tự động hoàn chỉnh (End-to-End)

**Mục tiêu:** Test toàn bộ workflow tự động từ đầu đến cuối

### Kịch bản:
**"Công ty tuyển nhân viên mới, thanh toán lương, phát sinh chi phí và tạo báo cáo"**

### Bước thực hiện:

#### Bước 1: Tuyển nhân viên mới
1. Tạo nhân viên `Trần Thị B` với đầy đủ thông tin
2. **Kiểm tra**: Bảng lương tự động tạo ✅

#### Bước 2: Điều chỉnh lương tháng đầu
1. Mở bảng lương của `Trần Thị B`
2. Cập nhật:
   - Lương cơ bản: `12,000,000`
   - Phụ cấp: `3,000,000`
   - Bảo hiểm: `1,200,000`
   - Thuế: `600,000`
3. Tổng lương: `13,200,000`
4. Save

#### Bước 3: Thanh toán lương
1. Chọn ngày thanh toán: Hôm nay
2. Chuyển trạng thái: `Đã thanh toán`
3. **Kiểm tra**: Phiếu chi lương tự động tạo ✅

#### Bước 4: Mua tài sản mới
1. Tạo tài sản `Máy in HP LaserJet` - 15,000,000đ
2. Tạo chi phí mua tài sản: 15,000,000đ
3. Duyệt chi phí
4. **Kiểm tra**: Phiếu chi tự động tạo ✅

#### Bước 5: Tài sản cần bảo trì
1. Tạo phiếu bảo trì cho `Máy in HP LaserJet` - 500,000đ
2. **Kiểm tra**: Chi phí bảo trì tự động tạo ✅
3. Duyệt chi phí bảo trì
4. **Kiểm tra**: Phiếu chi bảo trì tự động tạo ✅

#### Bước 6: Nhân viên mượn và làm hỏng tài sản
1. `Trần Thị B` mượn `Máy in HP LaserJet`
2. Trả lại với tình trạng `Hỏng`, phí bồi thường: 3,000,000đ
3. **Kiểm tra**: Chi phí bồi thường tự động tạo ✅
4. Duyệt chi phí bồi thường
5. **Kiểm tra**: Phiếu chi bồi thường tự động tạo ✅

#### Bước 7: Tạo báo cáo tổng hợp
1. Tạo báo cáo tài chính tháng này
2. **Kiểm tra**: 
   - Tổng chi lương: 13,200,000đ ✅
   - Tổng chi phí: 18,500,000đ ✅
   - Chi nhân sự, chi tài sản phân loại đúng ✅
   - Lãi/Lỗ tính đúng ✅

### Kết quả mong đợi:
✅ **7 bước tự động hóa** hoạt động liên hoàn  
✅ Không cần thao tác thủ công ở bất kỳ bước nào  
✅ Dữ liệu nhất quán xuyên suốt các module  
✅ Báo cáo real-time chính xác  

### Checklist tổng hợp:
- [ ] 1 nhân viên mới → 1 bảng lương tự động
- [ ] 1 lương thanh toán → 1 phiếu chi tự động
- [ ] 1 chi phí duyệt → 1 phiếu chi tự động
- [ ] 1 bảo trì → 1 chi phí tự động → 1 phiếu chi tự động
- [ ] 1 trả hỏng → 1 chi phí bồi thường → 1 phiếu chi tự động
- [ ] Tất cả phiếu chi → Báo cáo cập nhật tự động

---

# PHẦN 3: TEST HIỆU SUẤT VÀ KHẢ NĂNG

## ⚡ Test Case 3.1: Test với dữ liệu lớn

### Bước thực hiện:
1. Tạo **10 nhân viên mới** cùng lúc
2. Kiểm tra **10 bảng lương** tự động tạo
3. Thanh toán đồng loạt 10 bảng lương
4. Kiểm tra **10 phiếu chi** tự động tạo
5. Đo thời gian thực hiện

### Kết quả mong đợi:
✅ Tất cả automation hoạt động đúng với nhiều records  
✅ Không có lỗi race condition  
✅ Thời gian xử lý hợp lý (< 5 giây/record)  

---

## ⚡ Test Case 3.2: Test ràng buộc dữ liệu

### Test 1: Ngăn trùng lặp bảng lương
1. Tạo bảng lương thủ công cho `Nguyễn Văn A` - Tháng 2/2026
2. Thử tạo bảng lương thứ 2 cho cùng nhân viên - Tháng 2/2026
3. **Kết quả mong đợi**: Lỗi "Nhân viên đã có bảng lương trong tháng này!" ✅

### Test 2: Validation số tiền
1. Tạo chi phí với số tiền = 0
2. **Kết quả mong đợi**: Lỗi "Số tiền chi phí phải lớn hơn 0!" ✅

### Test 3: Validation tổng lương âm
1. Tạo bảng lương với khấu trừ > thu nhập
2. **Kết quả mong đợi**: Lỗi "Tổng lương không được âm!" ✅

---

# PHẦN 4: CHECKLIST TỔNG THỂ

## ✅ Mức 1: TÍCH HỢP HỆ THỐNG

| # | Yêu cầu | Cách kiểm tra | Kết quả |
|---|---------|---------------|---------|
| 1 | Chia sẻ chung Database | Tất cả bảng trong cùng DB | ⬜ |
| 2 | Nhân sự là dữ liệu gốc | Dropdown lấy từ module nhan_su | ⬜ |
| 3 | Không nhập trùng | Sửa 1 nơi, cập nhật mọi nơi | ⬜ |
| 4 | Tích hợp Nhân sự - Lương | Many2one relationship | ⬜ |
| 5 | Tích hợp Nhân sự - Chi phí | Many2one relationship | ⬜ |
| 6 | Tích hợp Tài sản - Chi phí | Many2one relationship | ⬜ |
| 7 | Tích hợp Nhân sự - Thu chi | Many2one relationship | ⬜ |

## ✅ Mức 2: TỰ ĐỘNG HÓA QUY TRÌNH

| # | Event | Automated Action | Kết quả |
|---|-------|------------------|---------|
| 1 | NV mới | → Tạo bảng lương | ⬜ |
| 2 | Thanh toán lương | → Tạo phiếu chi | ⬜ |
| 3 | Duyệt chi phí | → Tạo phiếu chi | ⬜ |
| 4 | Bảo trì tài sản | → Tạo chi phí | ⬜ |
| 5 | Trả tài sản hỏng | → Tạo chi phí bồi thường | ⬜ |
| 6 | Xác nhận phiếu | → Cập nhật báo cáo | ⬜ |
| 7 | Cuối tháng (cron) | → Tạo báo cáo tự động | ⬜ |

---

# PHẦN 5: BÁO CÁO KẾT QUẢ

## Mẫu báo cáo test

### Thông tin chung
- Người test: _______________
- Ngày test: _______________
- Phiên bản Odoo: 15.0
- Database: odoo

### Kết quả tổng hợp

**Mức 1: TÍCH HỢP HỆ THỐNG**
- Số test case: 5
- Passed: ___ / 5
- Failed: ___ / 5
- Tỷ lệ thành công: ____%

**Mức 2: TỰ ĐỘNG HÓA QUY TRÌNH**
- Số test case: 6
- Passed: ___ / 6
- Failed: ___ / 6
- Tỷ lệ thành công: ____%

### Lỗi phát hiện (nếu có)

| Test Case | Lỗi | Mức độ | Ghi chú |
|-----------|-----|--------|---------|
| TC X.X | Mô tả lỗi | Critical/Major/Minor | |

### Đánh giá chung

**Điểm mạnh:**
- ______________________
- ______________________

**Điểm cần cải thiện:**
- ______________________
- ______________________

**Kết luận:**
- [ ] ĐẠT Mức 1
- [ ] ĐẠT Mức 2
- [ ] Cần khắc phục lỗi

---

# PHỤ LỤC

## Câu lệnh SQL hữu ích

### Xem tất cả nhân viên và bảng lương
```sql
SELECT 
    nv.ho_va_ten,
    nv.email,
    bl.thang,
    bl.nam,
    bl.tong_luong,
    bl.trang_thai
FROM nhan_vien nv
LEFT JOIN bang_luong bl ON bl.nhan_vien_id = nv.id
ORDER BY nv.ho_va_ten, bl.nam DESC, bl.thang DESC;
```

### Xem workflow chi phí → phiếu chi
```sql
SELECT 
    cp.ma_chi_phi,
    cp.ten_chi_phi,
    cp.so_tien as chi_phi_so_tien,
    cp.trang_thai as chi_phi_trang_thai,
    tc.ma_phieu,
    tc.so_tien as phieu_chi_so_tien,
    tc.trang_thai as phieu_chi_trang_thai
FROM chi_phi cp
LEFT JOIN thu_chi tc ON tc.noi_dung LIKE CONCAT('%', cp.ma_chi_phi, '%')
ORDER BY cp.create_date DESC;
```

### Xem tổng hợp tự động hóa
```sql
-- Đếm các automation đã thực hiện
SELECT 
    'Nhân viên mới → Bảng lương' as automation,
    COUNT(*) as count
FROM bang_luong
WHERE ghi_chu LIKE '%tự động%'

UNION ALL

SELECT 
    'Chi phí → Phiếu chi',
    COUNT(*)
FROM thu_chi
WHERE ghi_chu LIKE '%tự động từ chi phí%'

UNION ALL

SELECT 
    'Lương → Phiếu chi',
    COUNT(*)
FROM thu_chi
WHERE ghi_chu LIKE '%tự động từ bảng lương%';
```

### Kiểm tra tính nhất quán dữ liệu
```sql
-- Kiểm tra email nhân viên có khớp giữa các bảng không
SELECT 
    nv.ho_va_ten,
    nv.email as email_nhan_su,
    bl.email as email_bang_luong,
    CASE 
        WHEN nv.email = bl.email THEN 'OK'
        ELSE 'NOT MATCH'
    END as kiem_tra
FROM nhan_vien nv
JOIN bang_luong bl ON bl.nhan_vien_id = nv.id;
```

---

## Tips để test hiệu quả

1. **Test từng bước**: Đừng bỏ qua bất kỳ test case nào
2. **Chụp screenshot**: Lưu bằng chứng cho mỗi automation
3. **Kiểm tra database**: Verify data ở cả UI và database
4. **Test negative cases**: Thử các trường hợp lỗi
5. **Clear cache**: Restart Odoo sau mỗi lần sửa code
6. **Check logs**: Xem terminal log khi automation chạy

---

## Liên hệ hỗ trợ

Nếu gặp vấn đề trong quá trình test:
1. Check Odoo log trong terminal
2. Check database trực tiếp
3. Kiểm tra lại cài đặt module
4. Review code trong file README.md

**Chúc test thành công! 🚀**
