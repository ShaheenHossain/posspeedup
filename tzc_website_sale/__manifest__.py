# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Shop For Portal TZC',
    'summary': 'Login To Access The Shop',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.0',
    'author': 'Odoo Inc',
    'description': """
eCommerce/Shop Restriction For Public User
==========================================
* What is the business use case for this development?
    - The customer is a B2B reseller. Only people that have a login can purchase from his webshop.
    - We should thus force the portal login to access the shop pages.
* Portal login required for every public user that tries to go to the /shop page. Even from a redirect.
    - So if on the website a link points to the /shop or subpage a login should be required
    """,
    'category': 'Custom Development',
    'depends': ['website_sale'],
    'data': [
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
