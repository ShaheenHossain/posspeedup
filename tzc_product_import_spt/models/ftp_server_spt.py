from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, Warning

import logging
_logger = logging.getLogger(__name__)
try:
    import paramiko
except ImportError:
    raise ImportError(
        'This module needs paramiko to automatically write backups to the FTP through SFTP. Please install paramiko on your system. (sudo pip3 install paramiko)')


class ftp_server_spt(models.Model):           
    _name = 'ftp.server.spt'
    _description = 'Server'

    name = fields.Char('Name')
    state = fields.Selection([('draft','Draft'),('confirm','Confirm')], 'State', default='draft')

    server_ip = fields.Char('Server IP')
    server_user = fields.Char('Server User')
    server_password = fields.Char('Server Password')
    server_port = fields.Integer('Server Port', default=22)

    @api.multi
    def test_connection(self, context=None):
        self.ensure_one()

        # Check if there is a success or fail and write messages
        messageTitle = ""
        messageContent = ""
        error = ""
        has_failed = False

        for rec in self:
            ipHost = rec.server_ip
            portHost = rec.server_port
            usernameLogin = rec.server_user
            passwordLogin = rec.server_password

            # Connect with external server over SFTP, so we know sure that everything works.
            try:
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(ipHost, portHost, usernameLogin, passwordLogin, timeout=10,allow_agent=False,look_for_keys=False)
                sftp = s.open_sftp()
                messageTitle = _("Connection Test Succeeded!\nEverything seems properly set up for FTP back-ups!")
            except Exception as e:
                _logger.critical('There was a problem connecting to the remote ftp: ' + str(e))
                error += str(e)
                has_failed = True
                messageTitle = _("Connection Test Failed!")
                if len(ipHost) < 8:
                    messageContent += "\nYour IP address seems to be too short.\n"
                messageContent += _("Here is what we got instead:\n")
            finally:
                if s:
                    s.close()

            if has_failed:
                raise Warning(messageTitle + '\n\n' + messageContent + "%s" % str(error))
            else:
                # raise Warning(messageTitle + '\n\n' + messageContent)
                rec.state = 'confirm'

    @api.multi
    def set_to_draft(self):
        for record in self:
            record.state = 'draft'