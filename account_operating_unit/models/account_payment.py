# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends("journal_id")
    def _compute_operating_unit_id(self):
        for payment in self:
            if payment.journal_id:
                payment.operating_unit_id = payment.journal_id.operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        domain="[('user_ids', '=', uid)]",
        compute="_compute_operating_unit_id",
        store=True,
    )

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super()._prepare_move_line_default_vals(write_off_line_vals)
        for line in res:
            line["operating_unit_id"] = self.operating_unit_id.id
        if self._context.get("active_model") and self._context.get("active_ids"):
            source_objects = self.env[self._context['active_model']].browse(self._context.get("active_ids"))
            if hasattr(source_objects, 'operating_unit_id'):
                source_ou = source_objects.operating_unit_id
                if source_objects and len(source_ou) == 1 and source_ou != self.operating_unit_id:
                    destination_account_id = self.destination_account_id.id
                    for line in res:
                        if line["account_id"] == destination_account_id:
                            line["operating_unit_id"] = source_ou.id
        return res
