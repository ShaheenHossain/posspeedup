# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################

from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    email_receipt = fields.Boolean("Email Receipt", default=False)
    update_record = fields.Boolean("Update Record", default=False)
    receipt_email = fields.Char("Receipt Email")
    email_client_id = fields.Many2one("res.partner")

    @api.model
    def order_formatLang(self,value,currency_obj=False):
        res = value
        if currency_obj and currency_obj.symbol:
            if currency_obj.position == 'after':
                res = u'%s\N{NO-BREAK SPACE}%s' % (res, currency_obj.symbol)
            elif currency_obj and currency_obj.position == 'before':
                res = u'%s\N{NO-BREAK SPACE}%s' % (currency_obj.symbol, res)
        return res
    
    @api.one
    def email_e_receipt(self):
        if self.update_record:
            if self.partner_id:
                self.partner_id.email = self.receipt_email
        ir_model_data = self.env['ir.model.data']
        temp_id=self.env.ref('pos_email_order_receipt.pos_e_receipt_email_template')
        if temp_id:
            res_id=self.id
            temp_id.send_mail(res_id,force_send=True)
        return True

    @api.model
    def create_from_ui(self, orders):
        order_ids = super(PosOrder, self).create_from_ui(orders)
        order_objs = self.browse(order_ids)
        for order_obj in order_objs:
            if order_obj.email_receipt:
                order_obj.email_e_receipt()
        return order_ids
    
    @api.model
    def _order_fields(self,ui_order):
        fields_return = super(PosOrder,self)._order_fields(ui_order)
        fields_return.update({'email_receipt':ui_order.get('email_receipt')})
        fields_return.update({'update_record':ui_order.get('update_record')})
        fields_return.update({'receipt_email':ui_order.get('receipt_email')})
        fields_return.update({'email_client_id':ui_order.get('email_client_id')})
        return fields_return