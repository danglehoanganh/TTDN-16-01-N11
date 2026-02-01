# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BaoTriSuaChuaExtend(models.Model):
    """
    Mở rộng model bao_tri_sua_chua từ module tai_san_doanh_nghiep
    Thêm tự động hóa: Khi bảo trì => Tự động tạo chi phí
    """
    _inherit = 'bao_tri_sua_chua'
    
    chi_phi_id = fields.Many2one('chi_phi', string="Chi phí tự động", readonly=True)
    
    # ============ MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH ============
    @api.model
    def create(self, vals):
        """
        TỰ ĐỘNG: Khi tạo phiếu bảo trì/sửa chữa tài sản
        => Tự động tạo Chi phí tài sản tương ứng
        """
        record = super(BaoTriSuaChuaExtend, self).create(vals)
        
        # Tự động tạo chi phí
        if record.ma_tai_san and hasattr(record, 'chi_phi') and record.chi_phi > 0:
            chi_phi = self.env['chi_phi'].create({
                'ten_chi_phi': f'Bảo trì/Sửa chữa - {record.ma_tai_san.ten_tai_san}',
                'loai_chi_phi': 'tai_san',
                'tai_san_id': record.ma_tai_san.id,
                'so_tien': record.chi_phi,
                'ngay_chi': record.ngay_bao_tri if hasattr(record, 'ngay_bao_tri') else fields.Date.today(),
                'trang_thai': 'cho_duyet',
                'mo_ta': f'Chi phí tự động từ bảo trì tài sản - {record.ma_tai_san.ma_tai_san}'
            })
            record.chi_phi_id = chi_phi.id
        
        return record


class MuonTraExtend(models.Model):
    """
    Mở rộng model muon_tra từ module tai_san_doanh_nghiep
    Thêm tự động hóa: Khi trả tài sản hỏng => Tự động tạo chi phí
    """
    _inherit = 'muon_tra'
    
    tinh_trang_tra = fields.Selection([
        ('binh_thuong', 'Bình thường'),
        ('hong', 'Hỏng'),
        ('mat', 'Mất'),
    ], string="Tình trạng khi trả")
    
    phi_boi_thuong = fields.Float("Phí bồi thường")
    chi_phi_id = fields.Many2one('chi_phi', string="Chi phí tự động", readonly=True)
    
    # ============ MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH ============
    def write(self, vals):
        """
        TỰ ĐỘNG: Khi trả tài sản với tình trạng "Hỏng" hoặc "Mất"
        => Tự động tạo Chi phí bồi thường
        """
        res = super(MuonTraExtend, self).write(vals)
        
        # Nếu tình trạng trả là hỏng/mất và có phí bồi thường
        if vals.get('tinh_trang_tra') in ['hong', 'mat'] and vals.get('phi_boi_thuong', 0) > 0:
            for record in self:
                if not record.chi_phi_id and record.nhan_vien_id:
                    # Tự động tạo chi phí bồi thường
                    chi_phi = self.env['chi_phi'].create({
                        'ten_chi_phi': f'Bồi thường tài sản {record.tinh_trang_tra} - {record.ma_tai_san.ten_tai_san}',
                        'loai_chi_phi': 'tai_san',
                        'nhan_vien_id': record.nhan_vien_id.id,
                        'tai_san_id': record.ma_tai_san.id,
                        'so_tien': record.phi_boi_thuong,
                        'ngay_chi': fields.Date.today(),
                        'trang_thai': 'cho_duyet',
                        'mo_ta': f'Chi phí bồi thường tự động - Tài sản {record.tinh_trang_tra} khi trả'
                    })
                    record.chi_phi_id = chi_phi.id
        
        return res
