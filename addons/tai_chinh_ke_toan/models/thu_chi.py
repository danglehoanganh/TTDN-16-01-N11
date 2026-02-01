# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ThuChi(models.Model):
    _name = 'thu_chi'
    _description = 'Quản lý thu chi'
    _rec_name = 'noi_dung'
    _order = 'ngay desc'

    ma_phieu = fields.Char("Mã phiếu", required=True, copy=False, readonly=True,
                            default=lambda self: 'TC' + fields.Datetime.now().strftime('%Y%m%d%H%M%S'))
    
    loai_phieu = fields.Selection([
        ('thu', 'Phiếu thu'),
        ('chi', 'Phiếu chi'),
    ], string="Loại phiếu", required=True)
    
    noi_dung = fields.Char("Nội dung", required=True)
    so_tien = fields.Float("Số tiền", required=True)
    ngay = fields.Date("Ngày", required=True, default=fields.Date.today)
    
    # TÍCH HỢP: Người nộp/nhận là nhân viên
    nhan_vien_id = fields.Many2one('nhan_vien', string="Người nộp/nhận")
    ho_ten = fields.Char(related='nhan_vien_id.ho_va_ten', string="Họ tên", store=True)
    
    hinh_thuc = fields.Selection([
        ('tien_mat', 'Tiền mặt'),
        ('chuyen_khoan', 'Chuyển khoản'),
        ('the', 'Thẻ'),
    ], string="Hình thức", required=True, default='tien_mat')
    
    nguoi_lap = fields.Many2one('nhan_vien', string="Người lập phiếu")
    ghi_chu = fields.Text("Ghi chú")
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Xác nhận'),
    ], string="Trạng thái", default='nhap')
    
    # ============ MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH ============
    def write(self, vals):
        """
        TỰ ĐỘNG: Khi phiếu thu/chi được xác nhận
        => Tự động trigger cập nhật báo cáo tài chính (nếu có)
        """
        res = super(ThuChi, self).write(vals)
        
        if vals.get('trang_thai') == 'xac_nhan':
            # Tự động cập nhật các báo cáo tài chính liên quan
            for record in self:
                bao_cao = self.env['bao_cao_tai_chinh'].search([
                    ('tu_ngay', '<=', record.ngay),
                    ('den_ngay', '>=', record.ngay)
                ])
                # Trigger recompute cho các báo cáo trong khoảng thời gian
                if bao_cao:
                    bao_cao._compute_tong_hop()
        
        return res
