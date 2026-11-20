# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    alias_domain_id = fields.Many2one("mail.alias.domain", string="Alias Domain")
    mail_server_id = fields.Many2one(
        comodel_name="ir.mail_server",
        string="Outgoing Mail Server",
        help=(
            "Preferred outgoing mail server for emails sent for records "
            "belonging to this operating unit."
        ),
    )
