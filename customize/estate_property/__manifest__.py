# -*- coding: utf-8 -*-
{
    'name': "estate_property",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Tutorial Odoo Server Framework 101 - Official
    """,

    'author': "Rohim Muhamad",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # Gunakan ini supaya modul bisa ditampilkan dengan filter 'Apps'
    'installable': True,
    'application': True,
}
