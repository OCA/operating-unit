# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _add_missing_default_values(self, values):
        if (
            not values.get("product_tmpl_id")
            and "company_id" in values
            and "categ_id" not in values
        ):
            # Delegated defaults are computed before the template is created.
            self = self.with_context(default_company_id=values["company_id"])  # noqa: PLW0642
        return super()._add_missing_default_values(values)
