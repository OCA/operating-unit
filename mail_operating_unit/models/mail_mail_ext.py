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
            operating_unit = False
            if mail.mail_message_id.model and mail.mail_message_id.res_id:
                model = mail.mail_message_id.model
                res_id = mail.mail_message_id.res_id
                record = self.env[model].browse(res_id)
                if getattr(record, 'operating_unit_id', False):
                    operating_unit = record.operating_unit_id
            if not operating_unit and self.env.context.get('uid', False):
                user = self.env['res.users'].browse(self.env.context.get('uid'))
                operating_unit = user.operating_unit_for_mails_id

            if operating_unit and operating_unit.catchall_alias and operating_unit.catchall_domain:
                sender_email_address = (operating_unit.catchall_alias + '@' +
                                        operating_unit.catchall_domain)
                email_name = operating_unit.partner_id.name
                mail.email_from = formataddr((email_name, sender_email_address))
                mail.reply_to = mail.email_from

                if operating_unit.outgoing_mail_server_id:
                    mail.mail_server_id = operating_unit.outgoing_mail_server_id.id

        return mails
