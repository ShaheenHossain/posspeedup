# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _

class product_template(models.Model):
    _inherit = 'product.template'

    brand = fields.Char('Brand')
    model = fields.Char('Model')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.display_name:
                record.display_name = record.name
        return super(product_template, self).name_get()
 