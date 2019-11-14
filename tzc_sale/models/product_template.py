# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare, pycompat
from odoo import tools

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_secondary = fields.Binary('Secondary Image', store=True)

    price_wholesale = fields.Float(
        'Wholesale Price',
        digits=dp.get_precision('Product Price'),
        help="Wholesale Price")

    price_msrp = fields.Float(
        'MSRP',
        digits=dp.get_precision('Product Price'),
        help="MSRP Price")

    

class ProductProduct(models.Model):
    _inherit = 'product.product'

    image_secondary = fields.Binary("Image Secondary", inverse='_set_image_secondary_value')

    @api.one
    def _set_image_secondary_value(self):

        if not self.product_tmpl_id.image_secondary:
            self.product_tmpl_id.image_secondary = self.image_secondary
