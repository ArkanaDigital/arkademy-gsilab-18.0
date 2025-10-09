# -*- coding: utf-8 -*-
{
    'name': "Safrial Latihan",

    'summary': "Modul perpustakaan dasar",

    'description': """
ini deskripsi lainnya
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'report_xlsx'
    ],

    # always loaded
    'data': [
        'security/library_groups.xml',
        'security/library_record_rules.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'data/safrial_library_data.xml',
        'views/library_category_views.xml',
        'views/library_author_views.xml',
        'views/res_partner_views.xml',
        'views/library_loan_views.xml',
        'views/library_member_views.xml',
        'wizard/library_borrow_wizard_views.xml',
        'reports/library_report.xml',
        'reports/library_book.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

