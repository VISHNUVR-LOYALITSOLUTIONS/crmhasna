# -*- coding: utf-8 -*-
{
    'name': "TDS Collection",

    'summary': """
       
        This module allows you to give the TDS in odoo payments 

        """,

    'description': """
        Tax deductible at source - The concept of TDS was introduced 
        with an aim to collect tax from the very source of income. 
        As per this concept, a person (deductor) who is liable to make 
        payment of specified nature to any other person (deductee) shall 
        deduct tax at source and remit the same into the account of the Central Government.
         The deductee from whose income tax has been deducted at source would be entitled to get 
         credit of the amount so deducted on the basis of Form 26AS or TDS certificate issued by the 
         deductor
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
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/account_payment_view.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/banner.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
