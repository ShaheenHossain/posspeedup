# -*- coding: utf-8 -*-

{
    'name': 'Pos Product Multi Image',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Webveer',
    'summary': 'Pos Multi Image allows you to show multiple product images.',
    'description': """

=======================

Pos Multi Image allows you to show multiple product images. 

""",
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/view.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 30,
    'currency': 'EUR',
}
