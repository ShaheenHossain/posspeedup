# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplateWizard(models.TransientModel):

    _name = 'product.template.wizard'

    # explicitly pass in context
    # def _default_products(self):
    #     return self.env['product.template'].browse(self.env.context.get('active_ids'))
    
    def _default_product_product(self):
        return self.env['product.product'].browse(self.env.context.get('active_ids'))

    # product_tmpl_ids = fields.Many2many('product.template', string="Selected Products", required=True, default=_default_products)

    product_pro_ids = fields.Many2many('product.product', 'product_product_template_wizard_rel_spt', 'wizard_id' , 'product_pro_id', string="Selected Products", required=True, default=_default_product_product)

    # catalog_line_ids = fields.Many2many('sale.catalog.line', string='Catalog Line')

    catalog_ids = fields.Many2many('sale.catalog', string='Add to Catalog(s)', required=True)

    @api.multi
    def add_products_to_catalogs(self):
        # sanity check
        # if self.product_tmpl_ids:
        #     raise ValidationError('YOOOO {}'.format(str(self.product_tmpl_ids)))

        if self.product_pro_ids and self.catalog_ids:
            # populate catalogs with these products
            for catalog_id in self.catalog_ids:
                # TODO: check if there are duplicates; and if this will erase prev product templates?
                # catalog_id.product_tmpl_ids = self.product_tmpl_ids.mapped('id')
                self.generate_catalog_lines(self.product_pro_ids, catalog_id)
                # print(catalog_id.product_tmpl_ids)

        return {'type': 'ir.actions.act_window_close'}

    def generate_catalog_lines(self, product_pro_ids, catalog_id):
        for product_pro_id in product_pro_ids:
            attribute_color = ''
            attribute_size = ''
            if product_pro_id.attribute_value_ids:
                for attribute in product_pro_id.attribute_value_ids:
                    if attribute.attribute_id.name == 'Size':
                        attribute_size = attribute.name + attribute_size
                    if attribute.attribute_id.display_name == 'Color':
                        attribute_color = attribute.name + attribute_color

            if not self.env['sale.catalog.line'].search([('catalog_id', '=', catalog_id.id), ('product_pro_id', '=', product_pro_id.id)]):
                line = self.env['sale.catalog.line'].create({
                    'catalog_id': catalog_id.id,
                    'product_pro_id': product_pro_id.id,
                    'product_price': product_pro_id.list_price,
                    'product_model' : product_pro_id.model,
                    'product_brand' : product_pro_id.brand,
                    'product_color' : attribute_color,
                    'product_size' : attribute_size

                })

