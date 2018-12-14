# -*- coding: utf-8 -*-
{
    'name': "cf_license",

    'summary': """
        许可证管理""",

    'description': """
        许可证管理。对收费odoo模块进行管理
    """,

    'author': "CFSoft Studio",
    'website': "http://www.khcloud.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'cfsoft',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,

}