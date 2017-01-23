# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# © 2015 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class CRMLead(models.Model):

    _inherit = 'crm.lead'

    @api.model
    def _get_default_operating_unit(self):
        team_id = self.env['crm.team']._get_default_team_id()
        team = self.env['crm.team'].sudo().browse(team_id)
        if team.operating_unit_id:
            return team.operating_unit_id
        else:
            return self.env['res.users'].operating_unit_default_get(self._uid)

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        related='team_id.operating_unit_id',
                                        default=_get_default_operating_unit)
