##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import api, models
from email.utils import formataddr


class MailMailExt(models.Model):
    _inherit = 'mail.mail'

    @api.model_create_multi
    def create(self, vals_list):
        mails = super(MailMailExt, self).create(vals_list)

        for mail in mails:
            if mail.mail_message_id.model and \
                    mail.mail_message_id.res_id:

                model = mail.mail_message_id.model
                res_id = mail.mail_message_id.res_id
                record = self.env[model].sudo().browse(res_id)

                sender_email_address = False
                if record.operating_unit_id and \
                        record.operating_unit_id.catchall_alias and \
                        record.operating_unit_id.catchall_domain:
                    sender_email_address = \
                        record.operating_unit_id.catchall_alias + '@' + \
                        record.operating_unit_id.catchall_domain

                outgoing_mail_server_id = False
                if record.operating_unit_id:
                    outgoing_mail_server_id = \
                        record.operating_unit_id.outgoing_mail_server_id

                if sender_email_address:
                    email_name = False
                    if record.operating_unit_id:
                        email_name = record.operating_unit_id.partner_id.name

                    mail.email_from = \
                        formataddr((email_name, sender_email_address))
                    mail.reply_to = mail.email_from

                if outgoing_mail_server_id:
                    mail.mail_server_id = outgoing_mail_server_id.id

        return mails
