# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    operating_unit_id = fields.Many2one(comodel_name="operating.unit")

    def _select_list(self, table):
        return super()._select_list(table) + [table.operating_unit_id]
