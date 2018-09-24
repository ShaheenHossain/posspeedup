# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    opened_from_catalog = fields.Boolean('Opened from a Sale Catalog', default=False)

    # @api.multi
    # def send_mail(self, auto_commit=False):
    #     mail = super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
    #     context = self._context
    #     if context.get('rapid_replacement_stage_update') and self.model == 'helpdesk.ticket' and context.get('active_ids'):
    #         ticket = self.env['helpdesk.ticket'].search([
    #             ('id', 'in', context.get('active_ids')),
    #             ('stage_id', 'in', [self.env.ref('mhd_helpdesk.stage_created_mhd').id, self.env.ref('mhd_helpdesk.stage_first_email_mhd').id])
    #         ])
    #
    #         if ticket.stage_id == self.env.ref('mhd_helpdesk.stage_created_mhd'):
    #             ticket.write({'stage_id': self.env.ref('mhd_helpdesk.stage_first_email_mhd').id})
    #         else:
    #             ticket.write({'stage_id': self.env.ref('mhd_helpdesk.stage_second_email_mhd').id})
    #         self = self.with_context(mail_post_autofollow=True)
    #     return mail