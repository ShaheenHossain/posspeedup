# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleCatalogLine(models.Model):
    _name = 'sale.catalog.line'

    catalog_id = fields.Many2one('sale.catalog', ondelete='cascade', string='Catalog', copy=False)
    product_tmpl_id = fields.Many2one('product.template', ondelete='cascade', string='Product', required=True)
    product_image = fields.Binary('Image', related='product_tmpl_id.image_small', readonly=True)
    product_uom_id = fields.Many2one('product.uom', related='product_tmpl_id.uom_id', readonly=True)
    product_price = fields.Float('Price', related='product_tmpl_id.list_price', readonly=True)
    product_price_to_customer = fields.Float('Price to Customer')
    product_qty = fields.Float('Qty', default=1.0)
    product_qty_at_date = fields.Float('Qty On Hand', related='product_tmpl_id.product_variant_id.qty_at_date', readonly=True)

    # TODO: add sql cosntraints
    # _sql_constrain = False

    @api.model
    def create(self, vals):
        rid = super(SaleCatalogLine, self).create(vals)
        if not rid.product_price_to_customer and rid.product_price:
            rid.product_price_to_customer = rid.product_price
        return rid


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
