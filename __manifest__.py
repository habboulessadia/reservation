# -*- coding: utf-8 -*-
{
    'name': "Booking management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','board','sale','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/booking_management_groups.xml',
        #'security/booking_management_security.xml',
        'views/booking_management_views.xml',
        'data/sequence_booking_management.xml',
        'views/actionServer.xml',
        'views/res_parntner_views.xml',
        'views/analyse_sale_order_views.xml',
        'views/sale_order_views.xml',
        'report/number_booking_report.xml',
        'report/number_canceled_booking_report.xml',
        'report/number_hours_booking_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
