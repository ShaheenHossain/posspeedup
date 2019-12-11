# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError

class pos_config(models.Model):
    _inherit = 'pos.config' 

    allow_partial_pay = fields.Boolean('Allow Partial Payment', default=True)
    min_amount = fields.Integer("Minimum amount(%)")

class pos_order(models.Model):
    _inherit = 'pos.order'
    
    reference_number = fields.Char()
    
    @api.model
    def _order_fields(self, ui_order):
        res = super(pos_order, self)._order_fields(ui_order)
        if 'reference_number' in ui_order:
            res['reference_number'] = ui_order['reference_number']
        return res

    @api.model
    def search_orders(self, refno):
        result = self.search([('reference_number','=',refno),('state','=','draft')])
        if result:
            return {
                'amount':result.amount_total - result.amount_paid,
                'name':result.name,
                'id':result.id,
            }

    @api.model
    def orderPayed(self, order_id, payment_ref,journal_id, amount):
        # order_obj = self.pool.get('pos.order')
        result = self.browse(int(order_id))
        context = {}
        data = {}
        data['journal'] = int(journal_id)
        data['amount'] = result.amount_total - result.amount_paid
        data['payment_name'] = payment_ref
        result.add_payment(data)
        if result.test_paid():
            result.action_pos_order_paid()


class PosSession(models.Model):
    _inherit = 'pos.session'


    def _confirm_orders(self):
        for session in self:
            company_id = session.config_id.journal_id.company_id.id
            orders = session.order_ids.filtered(lambda order: order.state == 'paid')
            journal_id = self.env['ir.config_parameter'].sudo().get_param(
                'pos.closing.journal_id_%s' % company_id, default=session.config_id.journal_id.id)
            if not journal_id:
                raise UserError(_("You have to set a Sale Journal for the POS:%s") % (session.config_id.name,))

            move = self.env['pos.order'].with_context(force_company=company_id)._create_account_move(session.start_at, session.name, int(journal_id), company_id)
            orders.with_context(force_company=company_id)._create_account_move_line(session, move)
            for order in session.order_ids.filtered(lambda o: o.state not in ['done', 'invoiced']):
                if order.state not in ('draft'):
                    order.action_pos_order_done()
            orders = session.order_ids.filtered(lambda order: order.state in ['invoiced', 'done'])
            orders.sudo()._reconcile_payments()

    @api.multi
    def action_pos_session_open(self):
        pos_order = self.env['pos.order'].search([('state', '=', 'draft')])
        for order in pos_order:
            if order.session_id.state != 'opened':
                order.write({'session_id': self.id})
        return super(PosSession, self).action_pos_session_open()

