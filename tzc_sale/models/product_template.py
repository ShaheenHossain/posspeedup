# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_secondary = fields.Binary('Secondary Image', compute='_compute_product_image_secondary', store=True)

    price_wholesale = fields.Float(
        'Wholesale Price',
        digits=dp.get_precision('Product Price'),
        help="Wholesale Price")

    price_msrp = fields.Float(
        'MSRP',
        digits=dp.get_precision('Product Price'),
        help="MSRP Price")

    @api.multi
    @api.depends('product_image_ids', 'product_image_ids.image')
    # set the secondary image to be the first image in the image list
    def _compute_product_image_secondary(self):
        for product in self:
            if product.product_image_ids.mapped('image'):
                product.image_secondary = product.product_image_ids[0].image
