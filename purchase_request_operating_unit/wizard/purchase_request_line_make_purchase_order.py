# Copyright 2016-19 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        string="Operating Unit",
        readonly=True,
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        operating_unit_id = False
        active_model = self.env.context.get("active_model", False)
        active_ids = self.env.context.get("active_ids", False)
        _model = {
            "purchase.request.line": "",
            "purchase.request": "line_ids",
        }
        request_lines = (
            self.env[active_model].browse(active_ids).mapped(_model[active_model])
        )
        for line in request_lines:
            line_operating_unit_id = (
                line.request_id.operating_unit_id
                and line.request_id.operating_unit_id.id
                or False
            )
            if operating_unit_id and line_operating_unit_id != operating_unit_id:
                raise ValidationError(
                    _(
                        "Could not process !"
                        "You have to select lines"
                        "from the same operating unit."
                    )
                )
            else:
                operating_unit_id = line_operating_unit_id
        res["operating_unit_id"] = operating_unit_id
        return res

    @api.model
    def _prepare_purchase_order(self, picking_type, location, company_id, origin):
        data = super()._prepare_purchase_order(
            picking_type, location, company_id, origin
        )
        if self.operating_unit_id:
            data["requesting_operating_unit_id"] = self.operating_unit_id.id
            data["operating_unit_id"] = self.operating_unit_id.id
        return data
