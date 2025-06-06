# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        check_company=True,
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
            lambda jl: jl.type in ("bank", "cash")
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
        amls = self.env["account.move.line"]
        line_datas = []
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
                line_datas.append(line_data)
        if line_datas:
            amls = self.with_context(check_move_validity=False).create(line_datas)
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


class AccountMove(models.Model):
    _inherit = "account.move"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        default=lambda self: self._default_operating_unit_id(),
        help="This operating unit will be defaulted in the move lines.",
        readonly=False,
        compute="_compute_operating_unit",
        store=True,
        check_company=True,
    )

    @api.model
    def _default_operating_unit_id(self):
        if (
            self._context.get("default_move_type", False)
            and self._context.get("default_move_type") != "entry"
        ):
            return self.env["res.users"]._get_default_operating_unit()
        return False

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

    @api.depends("journal_id")
    def _compute_operating_unit(self):
        for record in self:
            if record.journal_id.operating_unit_id:
                record.operating_unit_id = record.journal_id.operating_unit_id
                for line in record.line_ids:
                    line.operating_unit_id = record.journal_id.operating_unit_id

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
            amls = self.env["account.move.line"]
            line_datas = []
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
                    line_datas.append(line_data)
            if line_datas:
                amls = ml_obj.with_context(check_move_validity=False).create(line_datas)
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
