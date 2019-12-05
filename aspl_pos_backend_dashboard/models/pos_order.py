from odoo import api, fields, models, tools, _

class pos_order(models.Model):
    _inherit = "pos.order"

    amount_tax = fields.Float(compute='_compute_amount_all', string='Taxes', digits=0,store=True)
    amount_total = fields.Float(compute='_compute_amount_all', string='Total', digits=0,store=True)
    amount_paid = fields.Float(compute='_compute_amount_all', string='Paid', states={'draft': [('readonly', False)]}, readonly=True, digits=0,store=True)
    amount_return = fields.Float(compute='_compute_amount_all', string='Returned', digits=0,store=True)

    @api.depends('statement_ids', 'lines.price_subtotal_incl', 'lines.discount')
    def _compute_amount_all(self):
        for order in self:
            order.amount_paid = order.amount_return = order.amount_tax = 0.0
            currency = order.pricelist_id.currency_id
            order.amount_paid = sum(payment.amount for payment in order.statement_ids)
            order.amount_return = sum(payment.amount < 0 and payment.amount or 0 for payment in order.statement_ids)
            order.amount_tax = currency.round(sum(self._amount_line_tax(line, order.fiscal_position_id) for line in order.lines))
            amount_untaxed = currency.round(sum(line.price_subtotal for line in order.lines))
            order.amount_total = order.amount_tax + amount_untaxed