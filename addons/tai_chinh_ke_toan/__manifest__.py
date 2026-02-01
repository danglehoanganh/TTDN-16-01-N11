# -*- coding: utf-8 -*-
{
    'name': "Tài chính kế toán",

    'summary': """
        Quản lý tài chính kế toán doanh nghiệp tích hợp""",

    'description': """
        Module tài chính kế toán tích hợp với các module: Nhân sự, Tài sản, Văn bản
        - Quản lý lương nhân viên
        - Quản lý chi phí (nhân sự, tài sản, khác)
        - Quản lý thu chi
        - Báo cáo tài chính
        - Đồng bộ dữ liệu từ module Nhân sự làm gốc
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Accounting',
    'version': '0.1',
    'license': 'LGPL-3',

    # module phụ thuộc - tích hợp với các module khác
    'depends': ['base', 'nhan_su', 'tai_san_doanh_nghiep'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/automation_actions.xml',  # MỨC 2: Automated actions
        'views/bang_luong.xml',
        'views/chi_phi.xml',
        'views/thu_chi.xml',
        'views/bao_cao_tai_chinh.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
