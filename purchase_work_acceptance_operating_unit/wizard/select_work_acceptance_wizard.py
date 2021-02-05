# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SelectWorkAcceptanceWizard(models.TransientModel):
    _inherit = "select.work.acceptance.wizard"

    wa_id = fields.Many2one(
        comodel_name="work.acceptance",
        string="Work Acceptance",
        domain=lambda self: [
            ("state", "=", "accept"),
            ("purchase_id", "=", self._context.get("active_id")),
            (
                "operating_unit_id",
                "=",
                self.env["purchase.order"]
                .browse(self._context.get("active_id"))
                .operating_unit_id.id,
            ),
        ],
    )
