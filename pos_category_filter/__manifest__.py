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
  "name"                 :  "POS Category Filter",
  "summary"              :  "Ther module allows you to assign selected product categories to a POS. Only the products of the assigned categories will be displayed on the particular POS screen",
  "category"             :  "Point of Sale",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Category-Filter.html",
  "description"          :  """Odoo POS Category Filter
Separate products with category
POS Filter products
Category wise POS
Assign category filter to products
Product filters in POS
POS product sort
Sort products POS""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_category_filter",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_category_filter_view.xml',
                             'views/templates.xml',
                            ],
  "demo"                 :  ['data/pos_category_filter_demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}