# -*- coding: utf-8 -*-
# Part of SnepTech See LICENSE file for full copyright and licensing details.##
##################################################################################

{
    'name': "Product Importer",
    'summary': "",
    'sequence':1,
    'description': "",
    'category': '',
    'version': '11.0.0.1',
    'license': 'AGPL-3',
    'author': 'SnepTech',
    'website': 'https://www.sneptech.com',
    
    'depends': ['sale','sale_management','tzc_sale','tzc_website_sale'],

    'data': [
        'security/ir.model.access.csv',
        'data/action_image.xml',
        'data/seq.xml',
        'views/product_import_spt_view.xml',
        # 'views/ftp_server_spt_view.xml',
        'views/product_product_view.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
    
}
