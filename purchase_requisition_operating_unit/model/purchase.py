# © 2016 ForgeFlow S.L. (https://www.forgeflow.com)
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("requisition_id")
    def _onchange_requisition_id(self):
        super()._onchange_requisition_id()
        if self.requisition_id:
            self.requesting_operating_unit_id = self.requisition_id.operating_unit_id
            self.operating_unit_id = self.requisition_id.operating_unit_id
