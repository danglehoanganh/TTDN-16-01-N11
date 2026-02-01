# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương nhân viên'
    _rec_name = 'nhan_vien_id'
    _order = 'thang desc, nam desc'

    # TÍCH HỢP: Lấy dữ liệu nhân viên từ module nhan_su (dữ liệu gốc)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    
    # Thông tin đồng bộ từ nhân viên
    ho_ten = fields.Char(related='nhan_vien_id.ho_va_ten', string="Họ tên", store=True, readonly=True)
    email = fields.Char(related='nhan_vien_id.email', string="Email", store=True, readonly=True)
    
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12')
    ], string="Tháng", required=True)
    
    nam = fields.Integer("Năm", required=True, default=2026)
    
    # Các khoản lương
    luong_co_ban = fields.Float("Lương cơ bản", required=True, default=0)
    phu_cap = fields.Float("Phụ cấp", default=0)
    thuong = fields.Float("Thưởng", default=0)
    khau_tru = fields.Float("Khấu trừ", default=0)
    bao_hiem = fields.Float("Bảo hiểm", default=0)
    thue = fields.Float("Thuế TNCN", default=0)
    
    # Tính tổng lương thực nhận
    tong_luong = fields.Float("Tổng lương thực nhận", compute='_compute_tong_luong', store=True)
    
    trang_thai = fields.Selection([
        ('chua_thanh_toan', 'Chưa thanh toán'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", default='chua_thanh_toan')
    
    ngay_thanh_toan = fields.Date("Ngày thanh toán")
    ghi_chu = fields.Text("Ghi chú")
    
    @api.depends('luong_co_ban', 'phu_cap', 'thuong', 'khau_tru', 'bao_hiem', 'thue')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong = (record.luong_co_ban + record.phu_cap + record.thuong 
                                - record.khau_tru - record.bao_hiem - record.thue)
    
    @api.constrains('tong_luong')
    def _check_tong_luong(self):
        for record in self:
            if record.tong_luong < 0:
                raise ValidationError("Tổng lương không được âm!")
    
    # Ngăn trùng lặp: một nhân viên chỉ có 1 bảng lương/tháng
    _sql_constraints = [
        ('unique_nhan_vien_thang', 
         'unique(nhan_vien_id, thang, nam)', 
         'Nhân viên đã có bảng lương trong tháng này!')
    ]
    
    # ============ MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH ============
    def write(self, vals):
        """
        TỰ ĐỘNG: Khi bảng lương được đánh dấu "Đã thanh toán"
        => Tự động tạo Phiếu chi tương ứng
        """
        res = super(BangLuong, self).write(vals)
        
        # Nếu chuyển trạng thái sang "Đã thanh toán"
        if vals.get('trang_thai') == 'da_thanh_toan':
            for record in self:
                if record.ngay_thanh_toan:
                    # Tự động tạo phiếu chi lương
                    self.env['thu_chi'].create({
                        'loai_phieu': 'chi',
                        'noi_dung': f'Chi lương tháng {record.thang}/{record.nam} - {record.ho_ten}',
                        'so_tien': record.tong_luong,
                        'ngay': record.ngay_thanh_toan,
                        'nhan_vien_id': record.nhan_vien_id.id,
                        'hinh_thuc': 'chuyen_khoan',
                        'trang_thai': 'xac_nhan',
                        'ghi_chu': f'Phiếu chi tự động từ bảng lương {record.id}'
                    })
        
        return res
