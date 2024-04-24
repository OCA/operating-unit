# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("move_id", False):
                move = self.env["account.move"].browse(vals["move_id"])
                if move.operating_unit_id:
                    vals["operating_unit_id"] = move.operating_unit_id.id
        return super().create(vals_list)

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise UserError(
                    _(
                        "Configuration error. The Company in the"
                        " Move Line and in the Operating Unit must "
                        "be the same."
                    )
                )

    @api.constrains("operating_unit_id", "move_id")
    def _check_move_operating_unit(self):
        for rec in self:
            if (
                rec.move_id
                and rec.move_id.operating_unit_id
                and rec.operating_unit_id
                and rec.move_id.operating_unit_id != rec.operating_unit_id
            ):
                raise UserError(
                    _(
                        "Configuration error. The Operating Unit in"
                        " the Move Line and in the Move must be the"
                        " same."
                    )
                )

    def _check_ou_balance(self, lines):
        # Look for the balance of each OU
        ou_balance = {}
        for line in lines:
            if line.operating_unit_id.id not in ou_balance:
                ou_balance[line.operating_unit_id.id] = 0.0
            ou_balance[line.operating_unit_id.id] += line.credit - line.debit
        return ou_balance

    def reconcile(self):
        # if one OU pays the invoices of different OU
        # a regularization entry must be created (this
        # was a feature in version <= 12)
        if self and not self[0].company_id.ou_is_self_balanced:
            return super().reconcile()
        bank_journal = self.mapped("move_id.journal_id").filtered(
            lambda l: l.type in ("bank", "cash")
        )
        if not bank_journal:
            return super().reconcile()
        bank_journal = bank_journal[0]
        # If all move lines point to the same operating unit, there's no
        # need to create a balancing move line
        if len(self.mapped("operating_unit_id")) <= 1:
            return super().reconcile()
        # Create balancing entries for un-balanced OU's.
        move_vals = self._prepare_inter_ou_balancing_move(bank_journal)
        move = self.env["account.move"].create(move_vals)
        ou_balances = self._check_ou_balance(self)
        amls = []
        for ou_id in list(ou_balances.keys()):
            # If the OU is already balanced, then do not continue
            if move.company_id.currency_id.is_zero(ou_balances[ou_id]):
                continue
            # Create a balancing move line in the operating unit
            # clearing account
            line_data = move._prepare_inter_ou_balancing_move_line(
                move, ou_id, ou_balances
            )
            if line_data:
                amls.append(
                    self.with_context(check_move_validity=False).create(line_data)
                )
        if amls:
            move.with_context(check_move_validity=True).write(
                {"line_ids": [(4, aml.id) for aml in amls]}
            )
        move.with_context(inter_ou_balance_entry=True).action_post()
        return super().reconcile()

    def _prepare_inter_ou_balancing_move(self, journal):
        move_vals = {
            "journal_id": journal.id,
            "date": max(self.mapped("date")),
            "ref": "Inter OU Balancing",
            "company_id": journal.company_id.id,
        }
        return move_vals
