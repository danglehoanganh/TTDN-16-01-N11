# Module Tài chính Kế toán - Tích hợp Tự động hóa

## MỨC 1: TÍCH HỢP HỆ THỐNG
✅ Đã hoàn thành
- Chia sẻ chung database
- Nhân sự là dữ liệu gốc đồng bộ
- Loại bỏ nhập liệu trùng lặp

## MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH (Event-driven Automation)

### 1️⃣ Luồng tự động: Bảng lương → Phiếu chi
**Trigger:** Khi bảng lương được đánh dấu "Đã thanh toán"  
**Tự động:** Hệ thống tạo Phiếu chi lương tương ứng  
**File:** `models/bang_luong.py` - method `write()`

```
[Bảng lương] --thanh toán--> [Tự động tạo Phiếu chi]
```

### 2️⃣ Luồng tự động: Chi phí → Phiếu chi
**Trigger:** Khi chi phí được "Duyệt"  
**Tự động:** Hệ thống tạo Phiếu chi tương ứng  
**File:** `models/chi_phi.py` - method `write()`

```
[Chi phí] --duyệt--> [Tự động tạo Phiếu chi]
```

### 3️⃣ Luồng tự động: Bảo trì tài sản → Chi phí
**Trigger:** Khi tạo phiếu bảo trì/sửa chữa tài sản  
**Tự động:** Hệ thống tạo Chi phí tài sản  
**File:** `models/tai_san_extend.py` - model `BaoTriSuaChuaExtend`

```
[Bảo trì tài sản] --tạo--> [Tự động tạo Chi phí]
```

### 4️⃣ Luồng tự động: Trả tài sản hỏng/mất → Chi phí bồi thường
**Trigger:** Khi trả tài sản với tình trạng "Hỏng" hoặc "Mất"  
**Tự động:** Hệ thống tạo Chi phí bồi thường  
**File:** `models/tai_san_extend.py` - model `MuonTraExtend`

```
[Trả tài sản hỏng/mất] --cập nhật--> [Tự động tạo Chi phí bồi thường]
```

### 5️⃣ Luồng tự động: Nhân viên mới → Bảng lương
**Trigger:** Khi thêm nhân viên mới  
**Tự động:** Hệ thống tạo bảng lương tháng hiện tại  
**File:** `models/nhan_su_extend.py` - model `NhanVienExtend`

```
[Nhân viên mới] --tạo--> [Tự động tạo Bảng lương]
```

### 6️⃣ Luồng tự động: Phiếu thu/chi → Cập nhật báo cáo
**Trigger:** Khi phiếu thu/chi được xác nhận  
**Tự động:** Cập nhật các báo cáo tài chính liên quan  
**File:** `models/thu_chi.py` - method `write()`

```
[Phiếu thu/chi] --xác nhận--> [Tự động cập nhật Báo cáo]
```

### 7️⃣ Tự động hóa theo lịch: Báo cáo cuối tháng
**Trigger:** Cron job chạy hàng ngày  
**Tự động:** Tự động tạo báo cáo tài chính cuối tháng  
**File:** `data/automation_actions.xml`

```
[Cuối tháng] --scheduled--> [Tự động tạo Báo cáo tháng]
```

## Workflow tổng thể

```
┌─────────────┐     thanh toán      ┌──────────────┐
│ Bảng lương  │ ──────────────────> │  Phiếu chi   │
└─────────────┘                     └──────────────┘
                                            │
┌─────────────┐     duyệt                  │ xác nhận
│  Chi phí    │ ───────────────────────────┤
└─────────────┘                            │
      ▲                                    ▼
      │ tạo                      ┌──────────────────┐
┌─────────────┐                  │  Báo cáo tài     │
│ Bảo trì TS  │                  │     chính        │
└─────────────┘                  └──────────────────┘
                                          ▲
┌─────────────┐     tạo                  │
│ NV mới      │ ──────────────> [Bảng lương]
└─────────────┘
```

## Cách sử dụng

1. **Cài đặt:** Module tự động kích hoạt các luồng tự động hóa
2. **Không cần can thiệp thủ công:** Các tác vụ liên kết được thực hiện tự động
3. **Theo dõi:** Xem log và ghi chú tự động trong từng bản ghi

## Lợi ích

✅ Giảm thiểu thao tác thủ công  
✅ Đảm bảo tính nhất quán dữ liệu  
✅ Tránh sót quy trình  
✅ Tự động cập nhật báo cáo real-time  
✅ Tăng hiệu suất làm việc  
