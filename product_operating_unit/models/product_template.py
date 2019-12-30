# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _default_operating_unit_ids(self):
        if self.categ_id and self.categ_id.operating_unit_ids:
            return [(6, 0, self.categ_id.operating_unit_ids.ids)]
        return [(6, 0,
                 [self.env['res.users'].operating_unit_default_get(
                     self.env.uid).id])]

    operating_unit_ids = fields.Many2many(
        'operating.unit',
        'product_operating_unit_rel',
        string='Operating Units',
        default=_default_operating_unit_ids)

    @api.multi
    @api.constrains('operating_unit_ids', 'categ_id')
    def _check_operating_unit(self):
        for record in self:
            if record.categ_id.operating_unit_ids and \
                    not all(ou in record.operating_unit_ids.ids for
                            ou in record.categ_id.operating_unit_ids.ids):
                raise ValidationError(_(
                    "The operating units of the product must include the "
                    "ones from the category."))

    @api.multi
    @api.onchange('categ_id')
    def onchange_operating_unit_ids(self):
        for record in self:
            record.operating_unit_ids = \
                [(6, 0, record.categ_id.operating_unit_ids.ids)]
