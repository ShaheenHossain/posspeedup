# -*- coding: utf-8 -*-

{
    'name': 'Pos Product Variant Filter',
    'version': '11.0',
    'category': 'Point of Sale',
    'sequence': 1,
    'author': 'SNeptech',
    'summary': 'Pos Product variant filter.',
    'description': """

=======================

Allows you to filter the product by variant in POS. 

""",
    'depends': ['point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
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
    'price': 0.0,
    'currency': 'EUR',
}
