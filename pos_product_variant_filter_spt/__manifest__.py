# -*- coding: utf-8 -*-
#################################################################################
# Author      : Sneptech Pvt. Ltd. (<https://sneptech.com/>)
# Copyright(c): 2018-Present Sneptech Pvt. Ltd.
# All Rights Reserved.

{
    'name': 'Pos Product Variant Filter',
    'version': '11.0',
    'category': 'Point of Sale',
    'sequence': 1,
    'author': 'Sneptech',
    "website":  "https://sneptech.com",
    "license":  "Other proprietary",
    'summary': 'Pos Product variant filter.',
    'description': """

=======================

Allows you to filter the product by variants in POS. 

""",
    'depends': ['point_of_sale','tzc_product_import_spt'],
    'data': [
        # 'views/views.xml',
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/view.png',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',
    "application":  True,
}
