{
    'name': 'POS Product Ordering',
    'version': '11.0.1.0',
    'summary': 'Product Ordering for Point of Sale',
    'description': """
POS Product Ordering
====================

This module will allow cashier to order/sort POS products by name, name descending,
price and price descending.


Compatibility
-------------

This module is compatible and tested with these modules:
* Restaurant module (pos_restaurant)
* POS Discount module (pos_discount)


Keywords: Odoo POS Product Ordering, Odoo POS Product Sorting, Order by Name, Order by Price,
Sort by Name, Sort by Price, Odoo POS Ordering, Odoo POS Sorting, Odoo Ordering, Odoo Sorting
""",
    'category': 'Point of Sale',
    'author': 'MAC5',
    'contributors': ['MAC5'],
    'website': 'https://apps.odoo.com/apps/modules/browse?author=MAC5',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/pos_product_order_templates.xml',
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/pos_product_order_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [
        'static/description/pos_order_by_price_ascending.png',
        'static/description/pos_order_by_price_descending.png',
        'static/description/pos_order_by_name_ascending.png',
        'static/description/pos_order_by_name_descending.png',
    ],
    'price': 39.99,
    'currency': 'EUR',
    'support': 'mac5_odoo@outlook.com',
    'license': 'OPL-1',
}
