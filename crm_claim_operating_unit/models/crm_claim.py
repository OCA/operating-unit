# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# © 2015 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class CRMClaim(models.Model):

    _inherit = "crm.claim"

    @api.model
    def _default_operating_unit(self):
        team_id = self.env['crm.team']._get_default_team_id()
        team = self.env['crm.team'].sudo().browse(team_id)
        if team.operating_unit_id:
            for ou in self.env.user.operating_unit_ids:
                if ou.id == team.operating_unit_id.id:
                    return team.operating_unit_id
            return self.env.user.default_operating_unit_id
        else:
            return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=_default_operating_unit,
    )

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id:
            team = self.env['crm.team'].search([
                ('id', '=', self.team_id.id),
                ('operating_unit_id', 'in',
                 [g.id for g in self.env.user.operating_unit_ids])])
            if team:
                self.operating_unit_id = team.operating_unit_id
            else:
                self.team_id = False
                self.operating_unit_id = False

    @api.onchange('operating_unit_id')
    def onchange_operating_unit_id(self):
        if self.operating_unit_id:
            if self.operating_unit_id.id in \
                    [g.id for g in self.env.user.operating_unit_ids]:
                if ((not self.team_id) or
                        (self.team_id and self.team_id.operating_unit_id !=
                         self.operating_unit_id)):
                    team = self.env['crm.team'].search(
                        [('operating_unit_id', 'in',
                          [self.operating_unit_id.id])], limit=1)
                    if team:
                        self.team_id = team
                    else:
                        self.team_id = False
            else:
                self.team_id = False
                self.operating_unit_id = False

    @api.multi
    @api.constrains('team_id')
    def _check_team_operating_unit(self):
        for rec in self:
            if rec.operating_unit_id:
                if rec.team_id and rec.team_id.operating_unit_id != \
                        rec.operating_unit_id:
                    raise ValidationError(_('Configuration error\n'
                                            'The Operating Unit of the claim '
                                            'must match with that of the '
                                            'sales team.'))
            else:
                raise ValidationError(_('Configuration error\n'
                                        'The claim should be assigned to a '
                                        'sales team and the Operating Unit '
                                        'of the claim must match with that '
                                        'of the sales team.'))
