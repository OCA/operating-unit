# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountSpreadInvoiceLineLinkWizard(models.TransientModel):
    _inherit = "account.spread.invoice.line.link.wizard"

    def confirm(self):
        res = super().confirm()
        if self.spread_action_type == "new":
            ctx = res["context"]
            ctx.update(
                {
                    "default_operating_unit_id": self.invoice_line_id.operating_unit_id.id,
                }
            )
        return res
