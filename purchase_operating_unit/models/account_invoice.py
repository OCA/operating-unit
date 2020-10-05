# © 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, exceptions, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # Load all unsold PO lines
    @api.onchange("purchase_vendor_bill_id", "purchase_id")
    def _onchange_purchase_auto_complete(self):
        """
        Override to add Operating Unit from Purchase Order to Invoice.
        """
        purchase_id = self.purchase_id
        if self.purchase_vendor_bill_id.purchase_order_id:
            purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        if purchase_id and purchase_id.operating_unit_id:
            # Assign OU from PO to Invoice
            self.operating_unit_id = purchase_id.operating_unit_id.id
        return super()._onchange_purchase_auto_complete()

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit_id(self):
        """
        Show only the purchase orders that have the same operating unit
        """
        return {
            "domain": {
                "purchase_id": [("operating_unit_id", "=", self.operating_unit_id.id)]
            }
        }


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.constrains("operating_unit_id", "purchase_line_id")
    def _check_invoice_ou(self):
        for line in self:
            if (
                line.purchase_line_id
                and line.operating_unit_id != line.purchase_line_id.operating_unit_id
            ):
                raise exceptions.ValidationError(
                    _(
                        "The operating unit of the purchase order must "
                        "be the same as in the associated invoices."
                    )
                )
