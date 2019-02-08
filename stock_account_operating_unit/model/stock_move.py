# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, exceptions, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _prepare_account_move_line(self, qty, cost, credit_account_id,
                                   debit_account_id):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)
        if res:
            debit_line_vals = res[1][2]
            credit_line_vals = res[0][2]

            if (
                self.operating_unit_id and self.operating_unit_dest_id and
                self.operating_unit_id != self.operating_unit_dest_id and
                debit_line_vals['account_id'] != credit_line_vals['account_id']
            ):
                raise exceptions.UserError(
                    _('You cannot create stock moves involving separate source'
                      ' and destination accounts related to different '
                      'operating units.')
                )

            debit_line_vals['operating_unit_id'] = (
                self.operating_unit_dest_id.id or self.operating_unit_id.id
            )
            credit_line_vals['operating_unit_id'] = (
                self.operating_unit_id.id or self.operating_unit_dest_id.id
            )
            return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
        return res

    @api.multi
    def _action_done(self):
        """
        Generate accounting moves if the product being moved is subject
        to real_time valuation tracking,
        and the source or destination location are
        a transit location or is outside of the company or the source or
        destination locations belong to different operating units.
        """
        res = super(StockMove, self)._action_done()
        for move in self:

            if move.product_id.valuation == 'real_time':
                # Inter-operating unit moves do not accept to
                # from/to non-internal location
                if (
                        move.location_id.company_id ==
                        move.location_dest_id.company_id and
                        move.operating_unit_id != move.operating_unit_dest_id
                ):
                    src_company_ctx = dict(
                        force_company=move.location_id.company_id.id
                    )
                    company_ctx = dict(company_id=move.company_id.id)
                    self = self.with_context(src_company_ctx)
                    (journal_id, acc_src, acc_dest, acc_valuation) = \
                        move._get_accounting_data_for_valuation()

                    move_lines = move._prepare_account_move_line(
                        move.product_qty,
                        move.product_id.standard_price,
                        acc_valuation,
                        acc_valuation)
                    am = self.env["account.move"].with_context(
                        company_ctx).create({
                            'journal_id': journal_id,
                            'line_ids': move_lines,
                            'company_id': move.company_id.id,
                            'ref': move.picking_id and move.picking_id.name,
                            'stock_move_id': self.id,
                    })
                    am.post()
            return res
