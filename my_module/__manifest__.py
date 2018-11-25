# -*- coding: utf-8 -*-
{
    'name': "Library Books",

    'summary': """这一块是上面的描述，不可描述""",

    'description': """这一块不可描述""",

    'author': "My Company",
    'website': "http://www.baidu.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/library_book.xml',
        'security/groups.xml',
      #  'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 新加的字段，金额相关
    'name':'Chapter 05 code',
    'depends':['base','decimal_precision'],
    'data':['views/library_book.xml']
}