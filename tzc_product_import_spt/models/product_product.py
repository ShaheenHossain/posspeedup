# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _
import requests
import base64
from odoo.modules import get_module_resource

class product_product(models.Model):
    _inherit = 'product.product'

    image_url = fields.Char('Image URL')
    image_secondary_url = fields.Char('Image Secondary URL')
    number_of_variant = fields.Integer('Total Variant', related='product_tmpl_id.product_variant_count')
    default_code = fields.Char('Internal Reference', index=True, compute="_get_default_code")

    def refresh_images_product(self):
        self.onchange_image_url()
        self.onchange_image_secondary()

    @api.onchange('image_url')
    def onchange_image_url(self):
        for record in self:
            try:
                if not record.image_url:
                    raise UserError(_())
                res = requests.get(record.image_url.replace('\r',''))
                if res.ok:
                    image = base64.b64encode(res.content)
                    record.main_image = image
                else:
                    raise UserError(_())
            except:
                img_path = get_module_resource('tzc_product_import_spt', 'static/src/img', 'default_product_img.png')
                if img_path:
                    with open(img_path, 'rb') as f:
                        image = f.read()
                    record.main_image = base64.b64encode(image)

    @api.onchange('image_secondary_url')
    def onchange_image_secondary(self):
        for record in self:
            try:
                if not record.image_secondary_url:
                    raise UserError(_())
                res = requests.get(record.image_secondary_url.replace('\r',''))
                if res.ok:
                    image = base64.b64encode(res.content)
                    record.image_secondary = image
                else:
                    raise UserError(_())
            except:
                img_path = get_module_resource('tzc_product_import_spt', 'static/src/img', 'default_product_img.png')
                if img_path:
                    with open(img_path, 'rb') as f:
                        image = f.read()
                    record.image_secondary = base64.b64encode(image)
    
    def _get_default_code(self):
        for record in self:
            if record.barcode:
                record.default_code = record.barcode

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
    def action_open_variant_tree_spt(self):
        pass

    @api.multi
    def action_open_variant_spt(self):
        for record in self:
            # print(record.product_tmpl_id.env.ref('product.product_variant_action').read()[0])
            vals = self.env.ref('product.product_variant_action').read()[0]
            vals.update({'context':vals['context'].replace('active_id',str(record.product_tmpl_id.id))}) 
            return vals

    @api.multi
    def name_get(self):
        res = super(product_product, self).name_get()
        result = []
        for record in res:
            name = ''
            product_id = self.browse(record[0])
            if product_id:
                name = product_id.name
                if product_id.attribute_value_ids:
                    for attribute in product_id.attribute_value_ids:
                        name = name +' ' + attribute.name
                result.append((product_id.id, name))
        return result