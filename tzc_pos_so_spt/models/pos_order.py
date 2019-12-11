# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class pos_order(models.Model):
    _inherit = 'pos.order'

    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.multi
    def action_pos_order_paid(self):
        if not self.test_paid():
            raise UserError(_("Order is not paid."))
        self.write({'state': 'paid'})
        return True