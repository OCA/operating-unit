##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_operating_unit_ids(self):
        operating_unit = self.env['res.users'].operating_unit_default_get(
            self.env.uid)
        if operating_unit:
            return [(6, 0, [operating_unit.id])]
        else:
            return False

    operating_unit_ids = fields.Many2many(
        'operating.unit', relation='partner_operating_unit_rel',
        column1='partner_id', column2='operating_unit_id',
        string='Operating Unit',
        default=_default_operating_unit_ids
    )

    @api.constrains('operating_unit_ids', 'company_id')
    def _check_company_operating_unit(self):
        # operating_unit_ids is defined also on the res.partner, and
        # having two fields named equally on the 3rd type of inheritance
        # doesn't propagate the values. We do propagate manually, but the
        # constraint is checked before we can do the propagation, when the
        # partner is firstly created. Thus we skip the check in that case.
        if 'copy_ou_to_partner' in self.env.context:
            return True
        for record in self:
            if record.company_id and record.operating_unit_ids:
                for operating_unit in record.operating_unit_ids:
                    if record.company_id != operating_unit.company_id:
                        raise ValidationError(
                            _('Configuration error. The Company in the Contact'
                              ' and in the Operating Unit must be the same.'))
