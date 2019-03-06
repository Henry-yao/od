# -*- coding: utf-8 -*-
# name 为模块的名称 ，技术名称为模块目录名称（不要乱改目录名称，很多资源会乱掉）
#summary 对模块对概述
#description对模块对详细描述
#author 作者
#category 模块归类（没有太大的意义）
#version 版本号，11.0.0.1(odoo主版本.子版本.模块主版本.模块子版本)
#depends 模块依赖哪些东西
#data 要引入的数据文件
# security/ir.model.access.csv 权限控制文件

{
    'name': "ODOO开发培训",

    'summary': """ 广州众谛信息有限公司ODOO开发培训模块 """,

    'description': """   广州众谛信息有限公司ODOO开发培训模块    """,

    'author': " 众谛 ",
    'website': "http://www.zodioo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'training',
    'version': '11.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/training_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # application True的时候模型 会在应用显示出来
    'application':True

}