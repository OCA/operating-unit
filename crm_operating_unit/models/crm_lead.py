# Copyright 2019 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CRMLead(models.Model):

    _inherit = 'crm.lead'

    @api.model
    def _get_default_operating_unit(self):
        team = self.env['crm.team']._get_default_team_id()
        if team.operating_unit_id:
            return team.operating_unit_id
        return self.env['res.users'].operating_unit_default_get(self._uid)

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        related='team_id.operating_unit_id',
                                        readonly=True,
                                        default=_get_default_operating_unit)

    @api.constrains('operating_unit_id', 'user_id')
    def _check_users_operating_unit(self):
        for rec in self:
            if (rec.operating_unit_id and rec.user_id and
                    rec.operating_unit_id not in
                    rec.user_id.operating_unit_ids):
                raise ValidationError(_('Configuration Error. The User has '
                                        'not assigned the indicated Operating '
                                        'Unit.'))

    @api.constrains('user_id', 'team_id')
    def _check_salesperson_team(self):
        members = self.team_id.member_ids
        for rec in self:
            if rec.user_id and members.ids and \
                    rec.user_id.id not in members.ids:
                raise ValidationError(_('Configuration Error. The indicated '
                                        'Salesperson is not in the Sales '
                                        'Team.'))
