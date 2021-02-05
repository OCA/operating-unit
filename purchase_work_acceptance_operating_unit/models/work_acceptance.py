# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WorkAcceptance(models.Model):
    _inherit = "work.acceptance"

    READONLY_STATES = {
        "draft": [("readonly", False)],
        "accept": [("readonly", True)],
        "cancel": [("readonly", True)],
    }

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        states=READONLY_STATES,
        default=lambda self: (
            self.env["res.users"].operating_unit_default_get(self.env.uid)
        ),
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
                        "Configuration error. The Company in the Purchase Order "
                        "and in the Operating Unit must be the same."
                    )
                )


class WorkAcceptanceLine(models.Model):
    _inherit = "work.acceptance.line"

    operating_unit_id = fields.Many2one(
        related="wa_id.operating_unit_id", string="Operating Unit"
    )
