# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

from odoo.http import request
import logging
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float(track_visibility=True)

    price_wholesale = fields.Float(
        'Wholesale Price',
        digits=dp.get_precision('Product Price'),
        help="Wholesale Price")

    price_msrp = fields.Float(
        'MSRP',
        digits=dp.get_precision('Product Price'),
        help="MSRP Price")

    product_qty_available = fields.Float(related='product_id.product_tmpl_id.qty_available', readonly=True)

    product_image_secondary = fields.Binary(related='product_id.image_secondary')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    catalog_id = fields.Many2one('sale.catalog', ondelete='set null', string='Corresponding Catalog', track_visibility=True)
    order_line = fields.One2many(track_visibility='onchange')
    catalog_viewed = fields.Boolean('Catalog Viewed by Customer', default=False)
    # catalog_wizard_id = fields.Many2one('sale.catalog.wizard', ondelete='set null', string='Catalog Wizard')


    @api.multi
    def action_catalog_order_send(self):
        self.ensure_one()

        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('tzc_sale', 'email_template_catalog_quotation_tzc')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        # print('================================================================= preparing context')
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_opened_from_catalog': True,
            # 'default_composition_mode': 'comment',
            # mark so sent cannot be set for now, since it mess up the website catalog update
            'mark_so_as_sent': True,
            'custom_layout': 'sale.mail_template_data_notification_email_sale_order',
            # 'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def action_force_catalog_orders_send(self):
        for order in self:
            email_act = order.action_catalog_order_send()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                # email_ctx.update(default_email_from=order.company_id.email)
                order.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
        return True

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
            # print('entering')
            order_line = order._cart_find_product_line(product.id)
            # print(order_line)
            if order_line:
                # print('assigning')
                # pu = order_line.price_unit
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

        # qty_flag = 0
        # line_qty_available = 0.0

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
                    # order_line._get_display_price(product), we don't want the product price but the order_line price
                    order_line.price_unit,
                    order_line.product_id.taxes_id,
                    order_line.tax_id,
                    self.company_id
                )

            order_line.write(values)

        return {'line_id': order_line.id, 'quantity': quantity}



