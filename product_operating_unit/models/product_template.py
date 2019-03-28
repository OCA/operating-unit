##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _default_operating_unit_ids(self):
        return [(6, 0,
                 [self.env['res.users'].operating_unit_default_get(
                     self.env.uid).id])]

    operating_unit_ids = fields.Many2many(
        'operating.unit', 'product_operating_unit_rel',
        string='Operating Unit',
        default=_default_operating_unit_ids
    )

    @api.constrains('operating_unit_ids', 'company_id')
    def _check_company_operating_unit(self):
        for record in self:
            if record.company_id and record.operating_unit_ids:
                for operating_unit in record.operating_unit_ids:
                    if record.company_id != operating_unit.company_id:
                        raise ValidationError(
                            _('Configuration error. The Company in the Product'
                              ' and in the Operating Unit must be the same.')
                        )
