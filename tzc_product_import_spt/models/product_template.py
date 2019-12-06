# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _

class product_template(models.Model):
    _inherit = 'product.template'

    brand = fields.Char('Brand')
    model = fields.Char('Model')
    image_url = fields.Char('Image URL', compute='_get_image_and_url_secondary_template')
    image_secondary_url = fields.Char('Image Secondary URL', compute='_get_image_and_url_secondary_template')
    # image_secondary = fields.Binary('Secondary Image', store=True, compute='_get_image_and_url_secondary_template')

    def refresh_images_template(self):
        for record in self:
            record.product_variant_ids.refresh_images_product()

    def _get_image_and_url_secondary_template(self):
        for record in self:
            record.image_secondary = record.product_variant_id.image_secondary
            record.main_image = record.product_variant_id.main_image
            record.image_url = record.product_variant_id.image_url
            record.image_secondary_url = record.product_variant_id.image_secondary_url
    
