# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import fields, models

class PosConfig(models.Model):
	_inherit = 'pos.config'

	wk_product_category_ids = fields.Many2many('pos.category','config_category_relation','wk_config_id','wk_category_id',string="Product Categories")