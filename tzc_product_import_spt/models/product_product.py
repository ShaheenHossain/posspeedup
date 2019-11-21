# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _

class product_product(models.Model):
    _inherit = 'product.product'

    image_url = fields.Char('Image URL')
    image_secondary_url = fields.Char('Image Secondary URL')
    number_of_variant = fields.Integer('Total Variant', related='product_tmpl_id.product_variant_count')

    # def _get_number_of_variant(self):
    #     for record in self:
    #         record.number_of_variant = 

    def open_image_spt(self):
        self.ensure_one()
        if self.image_url:
            return {
                'type': 'ir.actions.act_url',
                'name': "Image",
                'target': 'new',
                'url': self.image_url,
            }

    def open_image_secondary_spt(self):
        self.ensure_one()
        if self.image_secondary_url:
            return {
                'type': 'ir.actions.act_url',
                'name': "Image",
                'target': 'new',
                'url': self.image_secondary_url,
            }

    @api.multi
    def action_open_variant_spt(self):
        for record in self:
            # print(record.product_tmpl_id.env.ref('product.product_variant_action').read()[0])
            vals = self.env.ref('product.product_variant_action').read()[0]
            vals.update({'context':vals['context'].replace('active_id',str(record.product_tmpl_id.id))}) 
            return vals