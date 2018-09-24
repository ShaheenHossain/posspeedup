# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, tools

from odoo.http import request

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    """
    Need a func that's similiar to sale_get_order()
    But this func should pull catalog related orders
    """
    @api.multi
    def sale_get_catalog_order(self):
        """
        :returns: browse record for the current sales order
        """
        self.ensure_one()
        partner = self.env.user.partner_id

        sale_order_ids = self.env['sale.order'].sudo().search([('partner_id', '=', partner.id), ('catalog_id', '!=', 'False'), ('state', 'in', ('draft', 'sent'))])

        if sale_order_ids:
            sale_order_id = sale_order_ids[0]

            if not request.session.get('sale_catalog_order_id'):
                request.session['sale_catalog_order_id'] = sale_order_id.id
            return sale_order_id
        return False

    def catalog_reset(self):
        request.session.update({
            'sale_catalog_order_id': False,
        })
