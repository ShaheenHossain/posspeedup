# -*- coding: utf-8 -*-


from odoo import fields, models,tools,api
import logging

class pos_product_variant_filter_spt(models.Model):
    _name = 'pos.multi.image'
    _order = "sequence desc"

    name = fields.Char('Name')
    image = fields.Binary('Image')
    sequence = fields.Integer("Sequence")
    pos_multi_img_id = fields.Many2one("Multi Img")

class product_product(models.Model):
    _inherit = 'product.product'

    product_multi_img_id = fields.One2many("pos.multi.image","pos_multi_img_id")

class pos_config(models.Model):
    _inherit = 'pos.config' 
    
    allow_multi_image = fields.Boolean(string='Allow multi image')
    