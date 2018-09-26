# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float(track_visibility=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    catalog_id = fields.Many2one('sale.catalog', ondelete='set null', string='Corresponding Catalog', track_visibility=True)
    order_line = fields.One2many(track_visibility='onchange')
    catalog_viewed = fields.Boolean('Catalog Viewed by Customer', default=False)
    # catalog_wizard_id = fields.Many2one('sale.catalog.wizard', ondelete='set null', string='Catalog Wizard')

    @api.multi
    def get_access_action(self, access_uid=None):
        """ Instead of the classic form view, redirect to the online order for
        portal users or if get_catalog=True in the context. """
        self.ensure_one()

        if self.state != 'cancel' and self.env.context.get('get_catalog'):
            user, record = self.env.user, self
            if access_uid:
                user = self.env['res.users'].sudo().browse(access_uid)
                record = self.sudo(user)

            if self.env.context.get('get_catalog'):

                return {
                    'type': 'ir.actions.act_url',
                    'url': '/shop/catalog',
                    'target': 'self',
                }

        return super(SaleOrder, self).get_access_action(access_uid)

    @api.multi
    def _website_product_id_change(self, order_id, product_id, qty=0):
        order = self.sudo().browse(order_id)
        product_context = dict(self.env.context)
        product_context.setdefault('lang', order.partner_id.lang)
        product_context.update({
            'partner': order.partner_id.id,
            'quantity': qty,
            'date': order.date_order,
            'pricelist': order.pricelist_id.id,
        })
        product = self.env['product.product'].with_context(product_context).browse(product_id)
        pu = product.price
        if order.pricelist_id and order.partner_id:
            order_line = order._cart_find_product_line(product.id)
            if order_line:
                pu = self.env['account.tax']._fix_tax_included_price_company(pu, product.taxes_id, order_line[0].tax_id, self.company_id)

        return {
            'product_id': product_id,
            'product_uom_qty': qty,
            'order_id': order_id,
            'product_uom': product.uom_id.id,
            'price_unit': pu,
            'product_qty_available': product.product_tmpl_id.qty_available,
        }

    @api.multi
    def _catalog_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        """ Add or set product quantity, add_qty can be negative """

        self.ensure_one()
        SaleOrderLineSudo = self.env['sale.order.line'].sudo()

        try:
            if add_qty:
                add_qty = float(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = float(set_qty)
        except ValueError:
            set_qty = 0
        quantity = 0
        order_line = False
        if self.state not in ('draft', 'sent'):
            request.session['sale_catalog_order_id'] = None
            raise UserError(_('It is forbidden to modify a sales order which is not in draft status'))
        if line_id is not False:
            order_lines = self._cart_find_product_line(product_id, line_id, **kwargs)
            order_line = order_lines and order_lines[0]

        qty_flag = 0

        # Create line if no line with product_id can be located

        # This should not happen for catalog unless this universe is actually crazy
        # if not order_line:
        #     values = self._website_product_id_change(self.id, product_id, qty=1)
        #     values['name'] = self._get_line_description(self.id, product_id, attributes=attributes)
        #     order_line = SaleOrderLineSudo.create(values)
        #
        #     try:
        #         order_line._compute_tax_id()
        #     except ValidationError as e:
        #         # The validation may occur in backend (eg: taxcloud) but should fail silently in frontend
        #         _logger.debug("ValidationError occurs during tax compute. %s" % (e))
        #     if add_qty:
        #         add_qty -= 1

        # compute new quantity
        if set_qty:
            quantity = set_qty
        elif add_qty is not None:
            quantity = order_line.product_uom_qty + (add_qty or 0)

        # Remove zero of negative lines
        if quantity <= 0:
            # todo: not sure this is desired - this behavior is conflicting the SO behavior?
            order_line.unlink()
        else:
            # update line
            values = self._website_product_id_change(self.id, product_id, qty=quantity)

            # check if qty is more than on hand
            requested_qty = values.get('product_uom_qty', False)
            available_qty = values.get('product_qty_available', False)
            if requested_qty:
                if not available_qty or requested_qty > available_qty:
                    values['product_uom_qty'] = available_qty
                    qty_flag = 1
            # del from dic after use
            if 'product_qty_available' in values:
                del values['product_qty_available']

            if self.pricelist_id.discount_policy == 'with_discount' and not self.env.context.get('fixed_price'):
                order = self.sudo().browse(self.id)
                product_context = dict(self.env.context)
                product_context.setdefault('lang', order.partner_id.lang)
                product_context.update({
                    'partner': order.partner_id.id,
                    'quantity': quantity,
                    'date': order.date_order,
                    'pricelist': order.pricelist_id.id,
                })
                product = self.env['product.product'].with_context(product_context).browse(product_id)
                values['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                    order_line._get_display_price(product),
                    order_line.product_id.taxes_id,
                    order_line.tax_id,
                    self.company_id
                )

            order_line.write(values)

        return {'line_id': order_line.id, 'quantity': quantity, 'qty_flag': qty_flag}



