# -*- coding: utf-8 -*-

{
    'name': 'POS Partial Payment',
    'version': '11.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Sneptech',
    'summary': 'POS Partial Payment Module',
    'description': """

=======================

This module allows you to pay partially for POS orders. 

""",
    'depends': ['point_of_sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/partialpay.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 39,
    'currency': 'EUR',
}
