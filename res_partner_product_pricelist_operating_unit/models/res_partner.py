# 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("operating_unit_ids")
    def _compute_product_pricelist(self):
        return super()._compute_product_pricelist()

    @api.constrains("operating_unit_ids", "property_product_pricelist")
    def _check_pricelist_operating_unit(self):
        for partner in self:
            pricelist = partner.property_product_pricelist
            if (
                pricelist
                and pricelist.operating_unit_id
                and partner.operating_unit_ids
                and pricelist.operating_unit_id not in partner.operating_unit_ids
            ):
                raise ValidationError(
                    _(
                        "Pricelist '%(pricelist)s' belongs to "
                        "Operating Unit '%(operating_unit)s' "
                        "which is not associated to this partner.",
                        pricelist=pricelist.name,
                        operating_unit=pricelist.operating_unit_id.name,
                    )
                )

    def _commercial_fields(self):
        # list of fields that are managed by the commercial entity
        # to which a partner belongs.
        return super()._commercial_fields() + ["operating_unit_ids"]
