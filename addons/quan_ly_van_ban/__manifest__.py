# -*- coding: utf-8 -*-
{
    'name': "Quản lý văn bản",

    'summary': """
        Quản lý văn bản đến và văn bản đi của tổ chức""",

    'description': """
        Module quản lý văn bản công văn đến/đi, theo dõi số hiệu, nơi gửi/nhận
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
        'views/van_ban_den.xml',
        'views/van_ban_di.xml',
        'views/muc_do_van_ban.xml',
        'views/menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
