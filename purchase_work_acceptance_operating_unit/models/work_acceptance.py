# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WorkAcceptance(models.Model):
    _inherit = "work.acceptance"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: (
            self.env["res.users"].operating_unit_default_get(self.env.uid)
        ),
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for record in self:
            if (
                record.company_id
                and record.operating_unit_id
                and record.company_id != record.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Company in the Work Acceptance "
                        "and in the Operating Unit must be the same."
                    )
                )

    @api.constrains("operating_unit_id", "purchase_id")
    def _check_purchase_order_operating_unit(self):
        for record in self:
            if (
                record.purchase_id
                and record.operating_unit_id
                and record.purchase_id.operating_unit_id != record.operating_unit_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Work Acceptance "
                        "and the Purchase Order must belong to the "
                        "same Operating Unit."
                    )
                )


class WorkAcceptanceLine(models.Model):
    _inherit = "work.acceptance.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        related="wa_id.operating_unit_id",
        store=True,
    )
