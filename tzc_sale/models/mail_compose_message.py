# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    opened_from_catalog = fields.Boolean('Opened from a Sale Catalog', default=False)

    @api.multi
    def send_mail(self, auto_commit=False):
        mail = super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
        context = self._context
        if context.get('catalog_orders'):
            order_ids = self.env['sale.order'].browse(context.get('catalog_orders'))
            order_ids.action_force_catalog_orders_send()

        self = self.with_context(mail_post_autofollow=True)
        return mail