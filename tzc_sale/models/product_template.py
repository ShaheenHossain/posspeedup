# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare, pycompat
from odoo import tools
import urllib
import base64
from odoo.modules import get_module_resource

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_secondary = fields.Binary('Secondary Image', compute='_get_image_and_url_secondary_template')

    price_wholesale = fields.Float(
        'Wholesale Price',
        digits=dp.get_precision('Product Price'),
        help="Wholesale Price")

    price_msrp = fields.Float(
        'MSRP',
        digits=dp.get_precision('Product Price'),
        help="MSRP Price")

    # def _get_image_and_url_secondary_template(self):
    #     for record in self:
    #         record.image_secondary = record.product_variant_id.image_secondary

class ProductProduct(models.Model):
    _inherit = 'product.product'

    image_secondary = fields.Binary("Image Secondary", compute="_get_image_secondary")
