# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RequestRequest(models.Model):

    _inherit = "request.request"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(),
    )
    child_request_ids = fields.Many2many(
        domain="[('state', '=', 'approved'),"
        "('operating_unit_id', '=', operating_unit_id)]",
    )

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit_id(self):
        self.child_request_ids = False

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for request in self:
            if (
                request.company_id
                and request.operating_unit_id
                and request.company_id != request.operating_unit_id.company_id
            ):
                raise UserError(
                    _(
                        "Configuration error, "
                        "The Company in the Request and in the "
                        "Operating Unit must be the same."
                    )
                )
