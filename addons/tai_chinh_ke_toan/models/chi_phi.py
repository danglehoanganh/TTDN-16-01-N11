# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ChiPhi(models.Model):
    _name = 'chi_phi'
    _description = 'Quản lý chi phí'
    _rec_name = 'ten_chi_phi'
    _order = 'ngay_chi desc'

    ma_chi_phi = fields.Char("Mã chi phí", required=True, copy=False, readonly=True, 
                              default=lambda self: 'CP' + fields.Datetime.now().strftime('%Y%m%d%H%M%S'))
    ten_chi_phi = fields.Char("Tên chi phí", required=True)
    
    loai_chi_phi = fields.Selection([
        ('nhan_su', 'Chi phí nhân sự'),
        ('tai_san', 'Chi phí tài sản'),
        ('van_phong', 'Chi phí văn phòng'),
        ('marketing', 'Chi phí marketing'),
        ('khac', 'Chi phí khác'),
    ], string="Loại chi phí", required=True)
    
    # TÍCH HỢP: Liên kết với nhân viên (nếu là chi phí liên quan nhân sự)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên liên quan")
    ho_ten = fields.Char(related='nhan_vien_id.ho_va_ten', string="Họ tên", store=True, readonly=True)
    
    # TÍCH HỢP: Liên kết với tài sản (nếu là chi phí bảo trì tài sản)
    tai_san_id = fields.Many2one('tai_san', string="Tài sản liên quan")
    ten_tai_san = fields.Char(related='tai_san_id.ten_tai_san', string="Tên tài sản", store=True, readonly=True)
    
    so_tien = fields.Float("Số tiền", required=True)
    ngay_chi = fields.Date("Ngày chi", required=True, default=fields.Date.today)
    nguoi_duyet = fields.Many2one('nhan_vien', string="Người duyệt")
    
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
    ], string="Trạng thái", default='cho_duyet')
    
    mo_ta = fields.Text("Mô tả chi tiết")
    file_dinh_kem = fields.Binary("File đính kèm")
    file_name = fields.Char("Tên file")
    
    @api.constrains('so_tien')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien <= 0:
                raise ValidationError("Số tiền chi phí phải lớn hơn 0!")
    
    # ============ MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH ============
    def write(self, vals):
        """
        TỰ ĐỘNG: Khi chi phí được "Duyệt"
        => Tự động tạo Phiếu chi tương ứng
        """
        res = super(ChiPhi, self).write(vals)
        
        # Nếu chuyển trạng thái sang "Đã duyệt"
        if vals.get('trang_thai') == 'da_duyet':
            for record in self:
                # Kiểm tra xem đã tạo phiếu chi chưa
                existing = self.env['thu_chi'].search([
                    ('noi_dung', 'ilike', f'Chi phí {record.ma_chi_phi}')
                ], limit=1)
                
                if not existing:
                    # Tự động tạo phiếu chi
                    self.env['thu_chi'].create({
                        'loai_phieu': 'chi',
                        'noi_dung': f'Chi phí {record.ma_chi_phi} - {record.ten_chi_phi}',
                        'so_tien': record.so_tien,
                        'ngay': record.ngay_chi,
                        'nhan_vien_id': record.nhan_vien_id.id if record.nhan_vien_id else False,
                        'hinh_thuc': 'tien_mat',
                        'trang_thai': 'xac_nhan',
                        'ghi_chu': f'Phiếu chi tự động từ chi phí {record.ma_chi_phi}'
                    })
        
        return res
    
    @api.model
    def create(self, vals):
        """
        TỰ ĐỘNG: Khi tạo chi phí từ tài sản bảo trì
        => Tự động liên kết với tài sản
        """
        record = super(ChiPhi, self).create(vals)
        return record
