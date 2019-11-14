# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleCatalogWizard(models.TransientModel):

    _name = 'sale.catalog.wizard'

    # explicitly pass in context
    def _default_catalogs(self):
        return self.env['sale.catalog'].browse(self.env.context.get('active_ids'))

    def _default_target_catalog(self):
        return self.catalog_ids[0] if self.catalog_ids else False

    catalog_ids = fields.Many2many('sale.catalog', string='Active Catalogs', required=True, default=_default_catalogs)
    target_catalog_id = fields.Many2one('sale.catalog', ondelet='cascade', string='Merge to Catalog', default=_default_target_catalog)
    selected_customer_ids = fields.Many2many('res.partner', string='Select Customers', required=True, domain=[('email', '!=', False)])

    template_id = fields.Many2one('mail.template', ondelete='set null')

    merge_archive = fields.Boolean('Archive Selected Catalogs after Merging', default=False)

    merge_type = fields.Selection([('merge_to_new', 'Merge to New Catalog'), ('merge_to_old', 'Merge to Existing Catalog')], string='Merge Type')


    @api.multi
    def open_email_composer(self):
        self.ensure_one()
        if not self.catalog_ids:
            return
        catalog_id = self.catalog_ids[0]
        if not catalog_id.line_ids:
            raise ValidationError(_('Cannot send empty catalog!'))
        if self.selected_customer_ids:
            # only use one customer as the representative in the email composer
            customer_rep_id = self.selected_customer_ids[0]
            # raise ValidationError(self.selected_customer_ids)

            customer_orders = {}

            # create Quotation for each customer
            for customer_id in self.selected_customer_ids:
                oid = self.env['sale.order'].create({
                    'partner_id': customer_id.id,
                    'catalog_id': catalog_id.id,
                    'template_id': False
                })
                # create SOLs
                for line_id in catalog_id.line_ids:
                    self.env['sale.order.line'].create({
                        'order_id': oid.id,
                        'product_id': line_id.product_tmpl_id.product_variant_id.id,
                        'price_unit': line_id.product_price,
                        'price_wholesale': line_id.product_price_wholesale,
                        'price_msrp': line_id.product_price_msrp,
                        'product_uom_qty': line_id.product_qty,
                        'product_uom': line_id.product_uom_id.id,
                    })
                customer_orders[customer_id] = oid

                # create user so that the customer can login to portal
                # if customer is already a user - make sure they have catalog access right
                sale_catalog_portal_group_id = self.env.ref('tzc_sale.group_sale_catalog_portal')
                if not customer_id.user_ids:
                    res_user_id = self.env['res.users'].sudo().create({
                        'name': customer_id.name,
                        'partner_id': customer_id.id,
                        'login': customer_id.email,
                        'groups_id': [(6, 0, [sale_catalog_portal_group_id.id])],
                    })
                else:
                    if sale_catalog_portal_group_id.id not in customer_id.mapped('user_ids').mapped('groups_id').mapped('id'):
                        customer_id.mapped('user_ids').write({'groups_id': [(4, sale_catalog_portal_group_id.id, 0)]})

            rep_order_id = customer_orders[customer_rep_id]
            catalog_orders = [o.id for o in list(customer_orders.values())[1:]]
            res = rep_order_id.action_catalog_order_send()
            if res and res.get('context') and catalog_orders:
                res['context']['catalog_orders'] = catalog_orders
            return res

    def _check_valid_merge(self):
        if len(self.catalog_ids) < 2:
            raise ValidationError(
                _('Merge only works for multiple catalogs. Please select at least 2 catalogs to proceed.'))
        if not self.target_catalog_id:
            raise ValidationError(
                _('Must select a destination catalog.')
            )
        # todo: if catalog lines have conflicting price and qty, should raise validation error?
        return True

    @api.multi
    def merge_catalogs(self):
        if self._check_valid_merge():
            # can you merge to a catalog that you did not select?
            # technically you can
            all_lines = self.catalog_ids.filtered(lambda c: c.id != self.target_catalog_id.id).mapped('line_ids')
            line_ids = []
            for line in all_lines:
                new_id = line.copy({'catalog_id': self.target_catalog_id.id})
                line_ids.append(new_id)

            # todo: ask what happens to related SOs? If a catalog is a merged target
            # todo: the related SOs would have no idea that their catalog is merged???
            # is this desire behavior? or should we set it so that it always merge to a new catalog?
            # we should never allow to merge to an existing catalog?

            if self.merge_archive:
                self.catalog_ids.filtered(lambda c: c.id != self.target_catalog_id.id).write({'active': False})

        return {'type': 'ir.actions.act_window_close'}


