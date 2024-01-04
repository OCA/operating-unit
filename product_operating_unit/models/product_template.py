# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


import logging

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, RedirectWarning, ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _default_operating_unit_ids(self):
        if self.categ_id and self.categ_id.operating_unit_ids:
            return [(6, 0, self.categ_id.operating_unit_ids.ids)]
        default_ou = self.env["res.users"].operating_unit_default_get(self.env.uid)
        if default_ou:
            return [
                (
                    6,
                    0,
                    default_ou.ids,
                )
            ]

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "product_operating_unit_rel",
        string="Operating Units",
        default=_default_operating_unit_ids,
    )

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

    @api.onchange("categ_id")
    def onchange_operating_unit_ids(self):
        for record in self:
            if record.categ_id.operating_unit_ids:
                record.operating_unit_ids = [
                    (6, 0, record.categ_id.operating_unit_ids.ids)
                ]

    def _get_default_category_id(self):
        for ou_id in self.env.user.operating_unit_ids:
            _logger.info("%s" % (ou_id.name))
            category = self.env["product.category"].search([], limit=1)
            if category:
                return category.id
            else:
                try:
                    self.env.ref(
                        "product.product_category_all", raise_if_not_found=False
                    ).name
                except AccessError as exc:
                    err_msg = _(
                        "You must define at least one product \
                        category within your Operating Unit in order to be \
                        able to create products."
                    )
                    redir_msg = _("Go to Product Categories")
                    raise RedirectWarning(
                        err_msg,
                        self.env.ref("product.product_category_action_form").id,
                        redir_msg,
                    ) from exc
                return super()._get_default_category_id()

    categ_id = fields.Many2one(
        "product.category",
        "Product Category",
        change_default=True,
        default=_get_default_category_id,
        required=True,
        help="Select category for the current product",
    )
