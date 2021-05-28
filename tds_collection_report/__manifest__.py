# -*- coding: utf-8 -*-
{
    'name': "TDS Excel Report",

    'summary': """
         This module allows you to give the TDS in odoo payments report in excel format. 
         """,

    'description': """
        This module allows you to generate the TDS in odoo payments report in excel format. 
        Which will help you for submit the report 
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': "13.0.1.0.0",
    'license': 'AGPL-3',
    'support': "support@loyalitsolutions.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'tds_collection'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/banner.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
