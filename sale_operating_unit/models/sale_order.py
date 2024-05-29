# © 2019 ForgeFlow S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        readonly=False,
        store=True,
        precompute=True,
        check_company=True,
        compute="_compute_operating_unit_id",
    )

    @api.depends("team_id")
    def _compute_operating_unit_id(self):
        for sale in self:
            if sale.team_id:
                sale.operating_unit_id = sale.team_id.operating_unit_id

    @api.depends("partner_id", "user_id", "operating_unit_id")
    def _compute_team_id(self):
        res = super()._compute_team_id()
        for order in self:
            if (
                order.team_id
                and order.team_id.operating_unit_id != order.operating_unit_id
            ):
                order.team_id = False
        return res

    @api.depends("operating_unit_id")
    def _compute_journal_id(self):
        res = super()._compute_journal_id()
        for sale in self:
            if not sale.journal_id or (
                sale.journal_id
                and sale.operating_unit_id
                and sale.journal_id.operating_unit_id != sale.operating_unit_id
            ):
                sale.journal_id = (
                    self.env["account.journal"]
                    .search(
                        [
                            "|",
                            ("operating_unit_id", "=", sale.operating_unit_id.id),
                            ("operating_unit_id", "=", False),
                            "|",
                            ("company_id", "=", sale.company_id.id),
                            ("company_id", "=", False),
                            ("type", "=", "sale"),
                        ],
                        limit=1,
                    )
                    .id
                )
        return res

    @api.constrains("team_id", "operating_unit_id")
    def _check_team_operating_unit(self):
        for rec in self:
            if rec.team_id and rec.team_id.operating_unit_id != rec.operating_unit_id:
                raise ValidationError(
                    _(
                        "Configuration error. The Operating "
                        "Unit of the sales team must match "
                        "with that of the quote/sales order."
                    )
                )

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        invoice_vals["operating_unit_id"] = self.operating_unit_id.id
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    operating_unit_id = fields.Many2one(
        related="order_id.operating_unit_id",
        string="Operating Unit",
        store=True,
    )
