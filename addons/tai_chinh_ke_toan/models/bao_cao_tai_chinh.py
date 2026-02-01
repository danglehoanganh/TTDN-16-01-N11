# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BaoCaoTaiChinh(models.Model):
    _name = 'bao_cao_tai_chinh'
    _description = 'Báo cáo tài chính tổng hợp'
    _rec_name = 'ten_bao_cao'
    _order = 'tu_ngay desc'

    ten_bao_cao = fields.Char("Tên báo cáo", required=True)
    loai_bao_cao = fields.Selection([
        ('thang', 'Báo cáo tháng'),
        ('quy', 'Báo cáo quý'),
        ('nam', 'Báo cáo năm'),
    ], string="Loại báo cáo", required=True, default='thang')
    
    tu_ngay = fields.Date("Từ ngày", required=True)
    den_ngay = fields.Date("Đến ngày", required=True)
    
    # TÍCH HỢP: Tổng hợp từ các module
    tong_chi_luong = fields.Float("Tổng chi lương", compute='_compute_tong_hop', store=True)
    tong_chi_phi = fields.Float("Tổng chi phí", compute='_compute_tong_hop', store=True)
    tong_thu = fields.Float("Tổng thu", compute='_compute_tong_hop', store=True)
    
    # Phân loại chi phí
    chi_nhan_su = fields.Float("Chi phí nhân sự", compute='_compute_tong_hop', store=True)
    chi_tai_san = fields.Float("Chi phí tài sản", compute='_compute_tong_hop', store=True)
    chi_khac = fields.Float("Chi phí khác", compute='_compute_tong_hop', store=True)
    
    # Kết quả
    lai_lo = fields.Float("Lãi/Lỗ", compute='_compute_tong_hop', store=True)
    
    nguoi_lap = fields.Many2one('nhan_vien', string="Người lập báo cáo")
    ngay_lap = fields.Date("Ngày lập", default=fields.Date.today)
    ghi_chu = fields.Text("Ghi chú")
    
    @api.depends('tu_ngay', 'den_ngay')
    def _compute_tong_hop(self):
        for record in self:
            # Tổng chi lương trong khoảng thời gian
            luong = self.env['bang_luong'].search([
                ('ngay_thanh_toan', '>=', record.tu_ngay),
                ('ngay_thanh_toan', '<=', record.den_ngay),
                ('trang_thai', '=', 'da_thanh_toan')
            ])
            record.tong_chi_luong = sum(luong.mapped('tong_luong'))
            
            # Tổng chi phí trong khoảng thời gian
            chi_phi = self.env['chi_phi'].search([
                ('ngay_chi', '>=', record.tu_ngay),
                ('ngay_chi', '<=', record.den_ngay),
                ('trang_thai', '=', 'da_duyet')
            ])
            record.tong_chi_phi = sum(chi_phi.mapped('so_tien'))
            
            # Phân loại chi phí
            record.chi_nhan_su = sum(chi_phi.filtered(lambda x: x.loai_chi_phi == 'nhan_su').mapped('so_tien'))
            record.chi_tai_san = sum(chi_phi.filtered(lambda x: x.loai_chi_phi == 'tai_san').mapped('so_tien'))
            record.chi_khac = record.tong_chi_phi - record.chi_nhan_su - record.chi_tai_san
            
            # Tổng thu trong khoảng thời gian
            thu = self.env['thu_chi'].search([
                ('ngay', '>=', record.tu_ngay),
                ('ngay', '<=', record.den_ngay),
                ('loai_phieu', '=', 'thu'),
                ('trang_thai', '=', 'xac_nhan')
            ])
            record.tong_thu = sum(thu.mapped('so_tien'))
            
            # Tính lãi/lỗ
            record.lai_lo = record.tong_thu - record.tong_chi_luong - record.tong_chi_phi
