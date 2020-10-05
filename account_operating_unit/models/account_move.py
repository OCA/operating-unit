# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit", domain="[('user_ids', '=', uid)]"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("move_id", False):
                move = self.env["account.move"].browse(vals["move_id"])
                if move.operating_unit_id:
                    vals["operating_unit_id"] = move.operating_unit_id.id
        return super().create(vals_list)

    @api.model
    def _query_get(self, domain=None):
        if domain is None:
            domain = []
        if self._context.get("operating_unit_ids", False):
            domain.append(
                ("operating_unit_id", "in", self._context.get("operating_unit_ids"))
            )
        return super()._query_get(domain)

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


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _default_operating_unit_id(self):
        if (
            self._context.get("default_type", False)
            and self._context.get("default_type") != "entry"
        ):
            return self.env["res.users"].operating_unit_default_get()
        return False

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        default=_default_operating_unit_id,
        domain="[('user_ids', '=', uid)]",
        help="This operating unit will be defaulted in the move lines.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_line_ids(self):
        res = super()._onchange_invoice_line_ids()
        if self.operating_unit_id:
            for line in self.line_ids:
                line.operating_unit_id = self.operating_unit_id
        return res

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
            "name": "OU-Balancing",
            "move_id": move.id,
            "journal_id": move.journal_id.id,
            "date": move.date,
            "operating_unit_id": ou_id,
            "account_id": move.company_id.inter_ou_clearing_account_id.id,
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

    def post(self):
        ml_obj = self.env["account.move.line"]
        for move in self:
            if not move.company_id.ou_is_self_balanced:
                continue

            # If all move lines point to the same operating unit, there's no
            # need to create a balancing move line
            ou_list_ids = {
                line.operating_unit_id and line.operating_unit_id.id
                for line in move.line_ids
                if line.operating_unit_id
            }
            if len(ou_list_ids) <= 1:
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
                    amls.append(ml_obj.with_context(wip=True).create(line_data))
            if amls:
                move.with_context(wip=False).write(
                    {"line_ids": [(4, aml.id) for aml in amls]}
                )

        return super().post()

    def _check_balanced(self):
        if self.env.context.get("wip"):
            return True
        return super()._check_balanced()

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
                # Change journal_id if create move from other model. e.g., sale.order
                if (
                    move._context.get("active_model")
                    and move._context.get("active_model") != "account.move"
                ):
                    move._onchange_operating_unit()
                    if (
                        move.journal_id.operating_unit_id
                        and move.operating_unit_id
                        and move.operating_unit_id != move.journal_id.operating_unit_id
                    ):
                        raise UserError(
                            _("The OU in the Move and in Journal must be the same.")
                        )
                else:
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
