##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import fields, models


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    def _default_operating_unit_ids(self):
        operating_unit = self.env['res.users'].operating_unit_default_get(
            self.env.uid)
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
