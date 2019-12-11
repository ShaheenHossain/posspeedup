# -*- coding: utf-8 -*-
# Part of SnepTech. See LICENSE file for full copyright and licensing details.##
###############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class pos_session(models.Model):
    _inherit = 'pos.session'

    @api.multi
    def action_pos_session_closing_control(self):
        res = super(pos_session, self).action_pos_session_closing_control()
        sale_order_obj = self.env['sale.order']
        for record in self:
            for pos_order in record.order_ids:
                line_vals = []
                for line in pos_order.lines:
                    line_vals.append((0,0,{
                        'product_id':line.product_id.id,
                        'product_uom_qty':line.qty,
                        'discount':line.discount,
                        'price_unit':line.price_unit,
                        'tax_id':[(6,0,line.tax_ids_after_fiscal_position.ids)]
                    }))
                sale_order = sale_order_obj.create({
                    'partner_id':pos_order.partner_id.id,
                    'order_line':line_vals,
                    'user_id':pos_order.user_id.id,
                })
                sale_order.action_confirm()
                if pos_order.invoice_id.id:
                    pos_order.invoice_id.origin = sale_order.name
                pos_order.sale_order_id = sale_order.id
            return res