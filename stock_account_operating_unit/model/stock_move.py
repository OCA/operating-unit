# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import _, api, exceptions, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _prepare_account_move_line(self, qty, cost, credit_account_id,
                                   debit_account_id):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)
        if res:
            debit_line_vals = res[0][2]
            credit_line_vals = res[1][2]

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
