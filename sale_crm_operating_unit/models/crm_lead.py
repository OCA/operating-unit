from odoo import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def action_sale_quotations_new(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id(
                "sale_crm.crm_quotation_partner_action"
            )
        if self.operating_unit_id:
            return self.with_context(
                default_operating_unit_id=self.operating_unit_id
            ).action_new_quotation()
        else:
            return self.action_new_quotation()
