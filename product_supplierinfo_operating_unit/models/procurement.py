# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(self, company_id, origin, values):
        res = super()._prepare_purchase_order(company_id, origin, values)
        operating_unit = self.location_id.operating_unit_id
        if not operating_unit and "sale_line_id" in values:
            operating_unit = (
                self.env["sale.order.line"]
                .browse(values["sale_line_id"])
                .order_id.operating_unit_id
            )
        if operating_unit:
            res.update(
                {
                    "operating_unit_id": operating_unit.id,
                    "requesting_operating_unit_id": operating_unit.id,
                }
            )
        return res

    def _run_buy(self, procurements):
        return super(
            StockRule,
            self.with_context(operating_unit=self.location_id.operating_unit_id),
        )._run_buy(procurements)
