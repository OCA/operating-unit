# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _default_operating_unit_id(self):
        if (
            self._context.get("default_move_type", False)
            and self._context.get("default_move_type") != "entry"
        ):
            return self.env["res.users"].operating_unit_default_get()
        return False

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        default=_default_operating_unit_id,
        help="This operating unit will be defaulted in the move lines.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit(self):
        if self.operating_unit_id and (
            not self.journal_id
            or self.journal_id.operating_unit_id != self.operating_unit_id
        ):
            journal = self.env["account.journal"].search(
                [("type", "=", self.journal_id.type)]
            )
            jf = journal.filtered(
                lambda aj: aj.operating_unit_id == self.operating_unit_id
            )
            if not jf:
                self.journal_id = journal[0]
            else:
                self.journal_id = jf[0]
            for line in self.line_ids:
                line.operating_unit_id = self.operating_unit_id

    @api.onchange("journal_id")
    def _onchange_journal(self):
        if (
            self.journal_id
            and self.journal_id.operating_unit_id
            and self.journal_id.operating_unit_id != self.operating_unit_id
        ):
            self.operating_unit_id = self.journal_id.operating_unit_id
            for line in self.line_ids:
                line.operating_unit_id = self.journal_id.operating_unit_id

    def _prepare_inter_ou_balancing_move_line(self, move, ou_id, ou_balances):
        if not move.company_id.inter_ou_clearing_account_id:
            raise UserError(
                _(
                    "Configuration error. You need to define an"
                    "inter-operating unit clearing account in the "
                    "company settings"
                )
            )

        res = {
            "name": _("OU-Balancing"),
            "move_id": move.id,
            "journal_id": move.journal_id.id,
            "date": move.date,
            "operating_unit_id": ou_id,
            "partner_id": move.partner_id and move.partner_id.id or False,
            "account_id": move.company_id.inter_ou_clearing_account_id.id,
            "display_type": "ou_balance",
        }

        if ou_balances[ou_id] < 0.0:
            res["debit"] = abs(ou_balances[ou_id])
        else:
            res["credit"] = ou_balances[ou_id]
        return res

    def _check_ou_balance(self, move):
        # Look for the balance of each OU
        ou_balance = {}
        for line in move.line_ids:
            if line.operating_unit_id.id not in ou_balance:
                ou_balance[line.operating_unit_id.id] = 0.0
            ou_balance[line.operating_unit_id.id] += line.debit - line.credit
        return ou_balance

    def _post(self, soft=True):
        ml_obj = self.env["account.move.line"]
        for move in self:
            if not move.company_id.ou_is_self_balanced or self.env.context.get(
                "inter_ou_balance_entry", False
            ):
                continue

            # If all move lines point to the same operating unit, there's no
            # need to create a balancing move line
            if len(move.line_ids.operating_unit_id) <= 1:
                continue
            # Create balancing entries for un-balanced OU's.
            ou_balances = self._check_ou_balance(move)
            amls = []
            for ou_id in list(ou_balances.keys()):
                # If the OU is already balanced, then do not continue
                if move.company_id.currency_id.is_zero(ou_balances[ou_id]):
                    continue
                # Create a balancing move line in the operating unit
                # clearing account
                line_data = self._prepare_inter_ou_balancing_move_line(
                    move, ou_id, ou_balances
                )
                if line_data:
                    amls.append(
                        ml_obj.with_context(check_move_validity=False).create(line_data)
                    )
            if amls:
                move.with_context(check_move_validity=True).write(
                    {"line_ids": [(4, aml.id) for aml in amls]}
                )

        return super()._post(soft)

    @api.constrains("line_ids")
    def _check_ou(self):
        for move in self:
            if not move.company_id.ou_is_self_balanced:
                continue
            for line in move.line_ids:
                if not line.operating_unit_id:
                    raise UserError(
                        _(
                            "Configuration error. The operating unit is "
                            "mandatory for each line as the operating unit "
                            "has been defined as self-balanced at company "
                            "level."
                        )
                    )

    @api.constrains("operating_unit_id", "journal_id")
    def _check_journal_operating_unit(self):
        for move in self:
            if (
                move.journal_id.operating_unit_id
                and move.operating_unit_id
                and move.operating_unit_id != move.journal_id.operating_unit_id
            ):
                raise UserError(
                    _("The OU in the Move and in Journal must be the same.")
                )
        return True

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for move in self:
            if (
                move.company_id
                and move.operating_unit_id
                and move.company_id != move.operating_unit_id.company_id
            ):
                raise UserError(
                    _(
                        "The Company in the Move and in "
                        "Operating Unit must be the same."
                    )
                )
        return True

    def button_draft(self):
        res = super().button_draft()
        for rec in self:
            rec.line_ids.filtered(lambda l: l.display_type == "ou_balance").unlink()
        return res
