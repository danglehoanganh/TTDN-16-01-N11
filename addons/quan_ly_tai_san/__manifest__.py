# -*- coding: utf-8 -*-
{
    'name': "Quản lý tài sản cá nhân",

    'summary': """
        Quản lý tài sản cá nhân: xe, nhà, đất, thu nhập""",

    'description': """
        Module quản lý tài sản cá nhân của người dân: phương tiện, nhà ở, mảnh đất, thu nhập
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/nhan_vat.xml',
        'views/phuong_tien.xml',
        'views/nha_o.xml',
        'views/manh_dat.xml',
        'views/thu_nhap.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
