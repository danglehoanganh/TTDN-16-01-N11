# -*- coding: utf-8 -*-
{
    'name': "Nhân sự",

    'summary': """
        Quản lý thông tin nhân viên và lý lịch""",

    'description': """
        Module quản lý nhân viên: thông tin cá nhân, chức vụ, đơn vị, lịch sử công tác, bằng cấp
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/nhan_vien.xml',
        'views/chucvu.xml',
        'views/donvi.xml',
        'views/lich_su_cong_tac.xml',
        'views/bangcap.xml',
        'views/quanlybangcap.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
