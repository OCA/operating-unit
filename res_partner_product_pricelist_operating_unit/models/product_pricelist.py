# 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def _get_partner_pricelist_multi(self, partner_ids):
        res = super()._get_partner_pricelist_multi(partner_ids)
        partners = self.env["res.partner"].browse(partner_ids).exists()
        partners_by_id = {partner.id: partner for partner in partners}

        for partner_id in res:
            partner = partners_by_id.get(partner_id)
            if not partner or not partner.operating_unit_ids:
                res[partner_id] = False
                continue

            pricelist_operating_unit = res[partner_id].operating_unit_id
            if (
                pricelist_operating_unit
                and pricelist_operating_unit not in partner.operating_unit_ids
            ):
                domain = self._get_product_pricelist_operating_unit_domain(partner)
                res[partner_id] = self.search(domain, limit=1) or False

        return res

    def _get_product_pricelist_operating_unit_domain(self, partner):
        domain = [
            ("operating_unit_id", "in", partner.operating_unit_ids.ids),
            ("company_id", "in", [self.env.company.id, False]),
            ("active", "=", True),
        ]
        return domain
