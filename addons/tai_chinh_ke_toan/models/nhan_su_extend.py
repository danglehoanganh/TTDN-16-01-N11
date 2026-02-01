# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienExtend(models.Model):
    """
    Mở rộng model nhan_vien từ module nhan_su
    Thêm tự động hóa: Khi thêm nhân viên mới => Tự động tạo bảng lương tháng hiện tại
    """
    _inherit = 'nhan_vien'
    
    tu_dong_tao_luong = fields.Boolean("Tự động tạo lương", default=True,
                                        help="Tự động tạo bảng lương khi thêm nhân viên mới")
    luong_co_ban_mac_dinh = fields.Float("Lương cơ bản mặc định", default=5000000)
    
    # ============ MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH ============
    @api.model
    def create(self, vals):
        """
        TỰ ĐỘNG: Khi tạo nhân viên mới
        => Tự động tạo bảng lương tháng hiện tại với lương cơ bản mặc định
        """
        record = super(NhanVienExtend, self).create(vals)
        
        # Nếu bật tự động tạo lương
        if record.tu_dong_tao_luong:
            today = fields.Date.today()
            thang = str(today.month)
            nam = today.year
            
            # Kiểm tra xem đã có bảng lương tháng này chưa
            existing = self.env['bang_luong'].search([
                ('nhan_vien_id', '=', record.id),
                ('thang', '=', thang),
                ('nam', '=', nam)
            ])
            
            if not existing:
                # Tự động tạo bảng lương
                self.env['bang_luong'].create({
                    'nhan_vien_id': record.id,
                    'thang': thang,
                    'nam': nam,
                    'luong_co_ban': record.luong_co_ban_mac_dinh or 5000000,
                    'phu_cap': 0,
                    'thuong': 0,
                    'khau_tru': 0,
                    'bao_hiem': 0,
                    'thue': 0,
                    'trang_thai': 'chua_thanh_toan',
                    'ghi_chu': 'Bảng lương tự động tạo cho nhân viên mới'
                })
        
        return record
