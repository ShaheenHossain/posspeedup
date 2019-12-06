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
  "name"                 :  "POS Order History & Re-Order",
  "summary"              :  "The module shows the order history for customers and allows the user to place same order again with a click.",
  "category"             :  "Point of Sale",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Order-History-Re-Order.html",
  "description"          :  """Odoo POS Order History & Re-Order
POS order history
POS re-order
POS reorder
POS previous order list
Last order pos
Previously bought products
POS Buy again""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_reorder",
  "depends"              :  ['pos_orders'],
  "data"                 :  ['views/template.xml'],
  "qweb"                 :  ['static/src/xml/*.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  13,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}