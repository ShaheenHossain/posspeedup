# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleCatalogLine(models.Model):
    _name = 'sale.catalog.line'

    catalog_id = fields.Many2one('sale.catalog', ondelete='cascade', string='Catalog', copy=False)
    product_tmpl_id = fields.Many2one('product.template', ondelete='cascade', string='Product', required=True)
    product_image = fields.Binary('Image', related='product_tmpl_id.image', readonly=True)
    product_image_secondary = fields.Binary('Secondary Image', related='product_tmpl_id.image_secondary', readonly=True)
    product_uom_id = fields.Many2one('product.uom', related='product_tmpl_id.uom_id', readonly=True)
    product_price = fields.Float('Our Price')  # this price pull from product list price, but can be modified
    product_price_msrp = fields.Float(related='product_tmpl_id.price_msrp', readonly=True)
    product_price_wholesale = fields.Float(related='product_tmpl_id.price_wholesale', readonly=True)
    product_qty = fields.Float('Qty', default=1.0)
    product_qty_available = fields.Float('Qty On Hand', related='product_tmpl_id.qty_available', readonly=True)


    # @api.model
    # def create(self, vals):
    #     rid = super(SaleCatalogLine, self).create(vals)
    #     return rid


class SaleCatalog(models.Model):
    _name = 'sale.catalog'

    name = fields.Char('Catalog Name', required=True)
    description = fields.Text('Description')
    # product_tmpl_ids = fields.Many2many('product.template', string='Products', help='Products in Current Catalog')
    line_ids = fields.One2many('sale.catalog.line', 'catalog_id', string='Catalog Lines')

    show_price = fields.Boolean('Show Price', default=True)
    show_qty = fields.Boolean('Show Quantity', default=True)

    order_ids = fields.One2many('sale.order', 'catalog_id', string='Generated SOs')

    sale_order_count = fields.Integer(compute='_get_sale_order_count')

    active = fields.Boolean('Active', default=True)

    @api.depends('order_ids')
    def _get_sale_order_count(self):
        for catalog in self:
            catalog.sale_order_count = len(catalog.order_ids)
