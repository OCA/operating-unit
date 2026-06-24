# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    operating_unit_id = fields.Many2one("operating.unit", string="Operating Unit")

    def _resolve_operating_unit_mail_server(self):
        """Assign the OU outgoing mail server on mails that have none.

        Iterates over mails without a ``mail_server_id`` that are linked to a
        record, and assigns the OU mail server when one can be resolved.
        Mails that already have a server set (e.g. from a template) are left
        untouched.
        """
        no_server_mails = self.filtered(
            lambda mail: not mail.mail_server_id and mail.model and mail.res_id
        )
        for mail in no_server_mails:
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

    def _split_by_mail_configuration(self):
        # OVERRIDE: pre-assign the OU mail server before grouping so the SMTP
        # session is opened on the correct server from the start.
        # See ``_resolve_operating_unit_mail_server()`` for the resolution logic.
        self._resolve_operating_unit_mail_server()
        return super()._split_by_mail_configuration()

    def _send(
        self,
        auto_commit=False,
        raise_exception=False,
        smtp_session=None,
        alias_domain_id=False,
    ):
        # SAFETY NET: ``_split_by_mail_configuration()`` already pre-assigns
        # ``mail_server_id`` from the OU before this method is called through the
        # normal ``send()`` flow, so this will typically be a no-op.
        # Kept as a fallback for any direct call to ``_send()`` that bypasses
        # ``_split_by_mail_configuration()``.
        self._resolve_operating_unit_mail_server()
        return super()._send(
            auto_commit=auto_commit,
            raise_exception=raise_exception,
            smtp_session=smtp_session,
            alias_domain_id=alias_domain_id,
        )
