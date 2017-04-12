# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class CRMTeam(models.Model):

    _inherit = "crm.team"

    @api.multi
    @api.constrains('operating_unit_id')
    def _check_team_operating_unit(self):
        for rec in self:
            claim = self.env['crm.claim'].search(
                [('team_id', '=', rec.id), ('operating_unit_id', '!=',
                                            rec.operating_unit_id.id)])
            if claim:
                raise ValidationError(_('Configuration error\n'
                                        'Claims already exists with another '
                                        'Operation Unit'))
