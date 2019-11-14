# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _

class product_template(models.Model):
    _inherit = 'product.template'

    brand = fields.Char('Brand')
    model = fields.Char('Model')