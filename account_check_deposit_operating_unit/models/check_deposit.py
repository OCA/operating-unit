# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountCheckDeposit(models.Model):
    _inherit = "account.check.deposit"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        related="journal_id.operating_unit_id",
        store=True,
        index=True,
    )
