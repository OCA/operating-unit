# Copyright 2016-19 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        string="Operating Unit",
        states={
            "to_approve": [("readonly", True)],
            "approved": [("readonly", True)],
            "done": [("readonly", True)],
        },
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        "The Company in the Purchase Request "
                        "and in the Operating Unit must be"
                        "the same."
                    )
                )

    @api.constrains("operating_unit_id", "picking_type_id")
    def _check_warehouse_operating_unit(self):
        for rec in self:
            picking_type = rec.picking_type_id
            if picking_type:
                if (
                    picking_type.warehouse_id
                    and picking_type.warehouse_id.operating_unit_id
                    and rec.operating_unit_id
                    and picking_type.warehouse_id.operating_unit_id
                    != rec.operating_unit_id
                ):
                    raise ValidationError(
                        _(
                            "Configuration error. The Purchase Request and the"
                            "Warehouse of picking type must belong to the same "
                            "Operating Unit."
                        )
                    )

    @api.constrains("operating_unit_id")
    def _check_approver_operating_unit(self):
        for rec in self:
            if (
                rec.assigned_to
                and rec.operating_unit_id
                and rec.operating_unit_id not in rec.assigned_to.operating_unit_ids
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The approver has not "
                        "the indicated Operating Unit"
                    )
                )


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        related="request_id.operating_unit_id",
        string="Operating Unit",
        store=True,
    )
