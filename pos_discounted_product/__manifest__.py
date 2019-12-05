# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Show Discounted Price",
  "summary"              :  "The module allows you to display the actual price that was and the new discounted price of the products in Odoo POS session.",
  "category"             :  "Point of Sale",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/OpenERP-POS-Discounted-Products.html",
  "description"          :  """Odoo POS Show Discounted Price
Show percentage discount
Discounted price POS
POS Price after discount POS
Instant discount Odoo
Odoo POS Order Discount
POS Order line discount
POS Orderline discount
Discount per product
POS Per product off
Odoo POS discount
Order discount
Fixed order line discount POS
Percentage discount odoo POS
Customer discount POS
Purchase discount 
Sales order discount
POS create discount
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_discounted_product",
  "depends"              :  [
                             'point_of_sale',
                             'sale',
                            ],
  "data"                 :  [],
  "demo"                 :  ['data/pos_discounted_product_demo.xml'],
  "qweb"                 :  ['static/src/xml/pos_dis_price.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  20,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}