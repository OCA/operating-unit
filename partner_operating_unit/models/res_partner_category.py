##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    def _default_operating_unit_ids(self):
        operating_unit = self.env['res.users'].operating_unit_default_get(self.env.uid)
        if operating_unit:
            return [(6, 0, [operating_unit.id])]
        else:
            return False

    operating_unit_ids = fields.Many2many(
        'operating.unit', relation='partner_categ_operating_unit_rel',
        column1='partner_categ_id', column2='operating_unit_id',
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
                            _('Configuration error. The Company in the Contact'
                              ' Tag and in the Operating Unit must be the '
                              ' same.'))
