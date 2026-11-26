# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Command


class ProductTemplate(models.Model):
    _inherit = "product.template"

    operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="product_operating_unit_rel",
        string="Operating Units",
        compute="_compute_operating_unit_ids",
        store=True,
        readonly=False,
    )

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        if "categ_id" not in fields or "categ_id" in defaults:
            return defaults

        if "company_id" in defaults:
            company_id = defaults["company_id"]
        else:
            company_id = super().default_get(["company_id"]).get("company_id")
        categories = self.env["product.category"]
        if categories.has_access("read"):
            category = categories.search(
                categories._check_company_domain(company_id), limit=1
            )
            if category:
                defaults["categ_id"] = category.id
        return defaults

    def _add_missing_default_values(self, values):
        if "company_id" in values and "categ_id" not in values:
            # The ORM only asks default_get for fields absent from the create values.
            self = self.with_context(default_company_id=values["company_id"])  # noqa: PLW0642
        return super()._add_missing_default_values(values)

    @api.constrains("operating_unit_ids", "categ_id")
    def _check_operating_unit(self):
        for record in self:
            if (
                record.operating_unit_ids and record.categ_id.operating_unit_ids
            ) and not all(
                ou in record.operating_unit_ids.ids
                for ou in record.categ_id.operating_unit_ids.ids
            ):
                raise ValidationError(
                    self.env._(
                        "The operating units of the product must include the "
                        "ones from the category."
                    )
                )

    @api.depends("categ_id")
    def _compute_operating_unit_ids(self):
        for record in self:
            record.operating_unit_ids = [
                Command.set(record.categ_id.operating_unit_ids.ids)
            ]
