# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    operating_unit_id = fields.Many2one("operating.unit", string="Operating Unit")

    def _send(
        self,
        auto_commit=False,
        raise_exception=False,
        smtp_session=None,
        alias_domain_id=False,
    ):
        # OVERRIDE: to assign an OU mail server when no explicit mail server is set.

        # Template mail server keeps the highest priority,
        # because it is already stored on ``mail.mail.mail_server_id``
        # before this method is called.
        no_mail_server_mails = self.filtered(
            lambda mail: not mail.mail_server_id and mail.model and mail.res_id
        )
        for mail in no_mail_server_mails:
            # Check if the related record actually exists,
            # as the mail could be linked to a deleted record.
            record = self.env[mail.model].browse(mail.res_id).exists()
            if not record:
                continue

            if mail_server := record._mail_get_operating_unit_mail_server():
                mail.write({"mail_server_id": mail_server.id})
                # Log the information about the resolved mail server
                # and the OU for each mail being sent.
                _logger.debug(
                    "mail_operating_unit: using operating unit mail server %s (%s) "
                    "from OU [%s] for record %s(%s)",
                    mail_server.display_name,
                    mail_server.id,
                    record._mail_get_operating_unit_label(),
                    record._name,
                    record.id,
                )
            else:
                _logger.debug(
                    "mail_operating_unit: no operating unit mail server resolved "
                    "from OU [%s] for record %s(%s), falling back to default behavior",
                    record._mail_get_operating_unit_label(),
                    record._name,
                    record.id,
                )

        return super()._send(
            auto_commit=auto_commit,
            raise_exception=raise_exception,
            smtp_session=smtp_session,
            alias_domain_id=alias_domain_id,
        )
