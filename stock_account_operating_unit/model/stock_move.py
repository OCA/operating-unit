# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, exceptions, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _generate_valuation_lines_data(
        self,
        partner_id,
        qty,
        debit_value,
        credit_value,
        debit_account_id,
        credit_account_id,
        svl_id,
        description,
    ):
        res = super()._generate_valuation_lines_data(
            partner_id,
            qty,
            debit_value,
            credit_value,
            debit_account_id,
            credit_account_id,
            svl_id,
            description,
        )
        if res:
            debit_line_vals = res.get("debit_line_vals")
            credit_line_vals = res.get("credit_line_vals")
            price_diff_line_vals = res.get("price_diff_line_vals", {})

            if (
                self.operating_unit_id
                and self.operating_unit_dest_id
                and self.operating_unit_id != self.operating_unit_dest_id
                and debit_line_vals["account_id"] != credit_line_vals["account_id"]
            ):
                raise exceptions.UserError(
                    _(
                        "You cannot create stock moves involving separate source"
                        " and destination accounts related to different "
                        "operating units."
                    )
                )

            if not self.operating_unit_dest_id and not self.operating_unit_id:
                ou_id = (
                    self.picking_id.picking_type_id.warehouse_id.operating_unit_id.id
                )
            else:
                ou_id = False

            debit_line_vals["operating_unit_id"] = (
                ou_id or self.operating_unit_dest_id.id or self.operating_unit_id.id
            )
            credit_line_vals["operating_unit_id"] = (
                ou_id or self.operating_unit_id.id or self.operating_unit_dest_id.id
            )
            rslt = {
                "credit_line_vals": credit_line_vals,
                "debit_line_vals": debit_line_vals,
            }
            if price_diff_line_vals:
                price_diff_line_vals["operating_unit_id"] = (
                    ou_id or self.operating_unit_id.id or self.operating_unit_dest_id.id
                )
                rslt["price_diff_line_vals"] = price_diff_line_vals
            return rslt
        return res
