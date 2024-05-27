# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models
from odoo.models import Command


class ProductCategory(models.Model):
    _inherit = "product.category"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "product_category_operating_unit_rel",
        string="Operating Units",
    )

    def write(self, vals):
        res = super().write(vals)
        product_template_obj = self.env["product.template"]
        if vals.get("operating_unit_ids"):
            for rec in self:
                products = product_template_obj.search(
                    [("categ_id", "child_of", rec.id)]
                )
                category_ou_ids = rec.operating_unit_ids
                for product in products:
                    ou_ids = product.operating_unit_ids | category_ou_ids
                    product.operating_unit_ids = [Command.set(ou_ids.ids)]
        return res
