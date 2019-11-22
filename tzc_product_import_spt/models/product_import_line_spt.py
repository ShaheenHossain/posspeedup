# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64

class product_import_line_spt(models.Model):
    _name = 'product.import.line.spt'

    name = fields.Char('Name')
    internal_reference = fields.Char('Internal Reference')
    is_active = fields.Boolean('Active')
    sale_ok = fields.Boolean('Sale Ok')
    purchase_ok = fields.Boolean('Purchase Ok')
    list_price = fields.Float('List Price')
    price_msrp = fields.Float('MSRP')
    standard_price = fields.Float('Standard Price')
    type = fields.Char('Type')
    barcode = fields.Char('Barcode')
    brand = fields.Char('Brand')
    model = fields.Char('Model')
    color = fields.Char('Color')
    size = fields.Char('Size')
    categ_id = fields.Char('Categ')
    image_1 = fields.Char('Image1')
    image_2 = fields.Char('Image2')
    image_1_url = fields.Char('Image1 URL')
    image_2_url = fields.Char('Image2 URL')

    import_id = fields.Many2one('product.import.spt', 'Product Import')
    

    # action_view_products