# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "product_operating_unit_rel",
        string="Operating Units",
        compute="_compute_operating_unit_ids",
        store=True,
        readonly=False,
    )
    categ_id = fields.Many2one(
        default=lambda self: self._get_default_category_id(),
    )

    def _get_default_category_id(self):
        category = self.env["product.category"].search([], limit=1)
        if category:
            return category.id
        else:
            return super()._get_default_category_id()

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
                    _(
                        "The operating units of the product must include the "
                        "ones from the category."
                    )
                )

    @api.depends("categ_id")
    def _compute_operating_unit_ids(self):
        for record in self:
            record.operating_unit_ids = [(6, 0, record.categ_id.operating_unit_ids.ids)]
