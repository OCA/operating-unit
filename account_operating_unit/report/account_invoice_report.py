# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountInvoiceReport(models.Model):

    _inherit = "account.invoice.report"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit", string="Operating Unit",
    )

    def _select(self):
        select_str = super()._select()
        select_str += """
            ,line.operating_unit_id
        """
        return select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += """
            ,line.operating_unit_id
        """
        return group_by_str
