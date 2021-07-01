# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# © 2021 O4SB Ltd - Rujia Liu
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, exceptions, models
from odoo.tools import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    def _create_in_svl(self, forced_quantity=None):
        svl_vals_list = []
        for move in self:
            move = move.with_company(move.company_id)
            valued_move_lines = move._get_in_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(
                    valued_move_line.qty_done, move.product_id.uom_id
                )
            unit_cost = abs(
                move._get_price_unit()
            )  # May be negative (i.e. decrease an out move).
            if move.product_id.cost_method == "standard":
                unit_cost = move.product_id.standard_price
            # use destination operating unit for incoming stock move
            svl_vals = move.product_id.with_context(
                operating_unit=move.operating_unit_dest_id.id
            )._prepare_in_svl_vals(forced_quantity or valued_quantity, unit_cost)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals["description"] = (
                    "Correction of %s (modification of past move)"
                    % move.picking_id.name
                    or move.name
                )
            svl_vals_list.append(svl_vals)
        return self.env["stock.valuation.layer"].sudo().create(svl_vals_list)

    def _create_out_svl(self, forced_quantity=None):
        svl_vals_list = []
        for move in self:
            move = move.with_company(move.company_id)
            valued_move_lines = move._get_out_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(
                    valued_move_line.qty_done, move.product_id.uom_id
                )
            if float_is_zero(
                forced_quantity or valued_quantity,
                precision_rounding=move.product_id.uom_id.rounding,
            ):
                continue
            # use source operating unit for outgoing stock move
            svl_vals = move.product_id.with_context(
                operating_unit=move.operating_unit_id.id
            )._prepare_out_svl_vals(forced_quantity or valued_quantity, move.company_id)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals["description"] = (
                    "Correction of %s (modification of past move)"
                    % move.picking_id.name
                    or move.name
                )
            svl_vals["description"] += svl_vals.pop("rounding_adjustment", "")
            svl_vals_list.append(svl_vals)
        return self.env["stock.valuation.layer"].sudo().create(svl_vals_list)

    def _create_dropshipped_svl(self, forced_quantity=None):
        svl_vals_list = []
        for move in self:
            move = move.with_company(move.company_id)
            valued_move_lines = move.move_line_ids
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(
                    valued_move_line.qty_done, move.product_id.uom_id
                )
            quantity = forced_quantity or valued_quantity

            unit_cost = move._get_price_unit()
            if move.product_id.cost_method == "standard":
                unit_cost = move.product_id.standard_price

            common_vals = dict(move._prepare_common_svl_vals(), remaining_qty=0)
            common_vals["operating_unit_id"] = move.picking_id.operating_unit_id.id

            # create the in
            in_vals = {
                "unit_cost": unit_cost,
                "value": unit_cost * quantity,
                "quantity": quantity,
            }
            in_vals.update(common_vals)
            svl_vals_list.append(in_vals)

            # create the out
            out_vals = {
                "unit_cost": unit_cost,
                "value": unit_cost * quantity * -1,
                "quantity": quantity * -1,
            }
            out_vals.update(common_vals)
            svl_vals_list.append(out_vals)
        return self.env["stock.valuation.layer"].sudo().create(svl_vals_list)

    def _generate_valuation_lines_data(
        self,
        partner_id,
        qty,
        debit_value,
        credit_value,
        debit_account_id,
        credit_account_id,
        description,
    ):
        rslt = super(StockMove, self)._generate_valuation_lines_data(
            partner_id,
            qty,
            debit_value,
            credit_value,
            debit_account_id,
            credit_account_id,
            description,
        )
        if rslt:
            debit_line_vals = rslt.get("debit_line_vals")
            credit_line_vals = rslt.get("credit_line_vals")
            price_diff_line_vals = rslt.get("price_diff_line_vals", {})

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
            rslt["credit_line_vals"] = credit_line_vals
            rslt["debit_line_vals"] = debit_line_vals
            if price_diff_line_vals:
                price_diff_line_vals["operating_unit_id"] = (
                    ou_id or self.operating_unit_id.id or self.operating_unit_dest_id.id
                )
                rslt["price_diff_line_vals"] = price_diff_line_vals
        return rslt

    def _action_done(self, cancel_backorder=False):
        """
        Generate accounting moves if the product being moved is subject
        to real_time valuation tracking,
        and the source or destination location are
        a transit location or is outside of the company or the source or
        destination locations belong to different operating units.
        """
        res = super(StockMove, self)._action_done(cancel_backorder)
        for move in self:

            if move.product_id.valuation == "real_time":
                # Inter-operating unit moves do not accept to
                # from/to non-internal location
                if (
                    move.location_id.company_id
                    and move.location_id.company_id == move.location_dest_id.company_id
                    and move.operating_unit_id != move.operating_unit_dest_id
                ):
                    (
                        journal_id,
                        acc_src,
                        acc_dest,
                        acc_valuation,
                    ) = move._get_accounting_data_for_valuation()

                    move_lines = move._prepare_account_move_line(
                        move.product_qty,
                        move.product_id.standard_price,
                        acc_valuation,
                        acc_valuation,
                        _("%s - OU Move") % move.product_id.display_name,
                    )
                    am = (
                        self.env["account.move"]
                        .with_context(
                            company_id=move.company_id.id,
                        )
                        .with_company(move.location_id.company_id.id)
                        .create(
                            {
                                "journal_id": journal_id,
                                "line_ids": move_lines,
                                "company_id": move.company_id.id,
                                "ref": move.picking_id and move.picking_id.name,
                                "stock_move_id": move.id,
                            }
                        )
                    )
                    am.action_post()
            return res
