# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    operating_unit_id = fields.Many2one("operating.unit", string="Operating Unit")

    def send_mail(
        self, res_id, force_send=False, raise_exception=False, email_values=None
    ):
        # Include in the email values the alias domain ID of the current OU if any
        email_values = email_values or {}
        if self.operating_unit_id and self.operating_unit_id.alias_domain_id:
            email_values["record_alias_domain_id"] = (
                self.operating_unit_id.alias_domain_id.id,
            )
        return super().send_mail(
            res_id,
            force_send=force_send,
            raise_exception=raise_exception,
            email_values=email_values,
        )
