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
  "name"                 :  "POS Email Receipt",
  "summary"              :  "This module allows the seller to send an e-receipt to the customers via email instead of printing one.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/POS-Email-Receipt.html",
  "description"          :  """This module allows the seller to send an e-receipt to the customers via email instead of printing one.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_email_order_receipt&version=11.0&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                              'views/template.xml',
                              'reports/e_receipt_paperformat.xml',
                              'reports/report_file.xml',
                              'reports/order_report.xml',
                              'edi/pos_email_receipt.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}