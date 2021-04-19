# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    @api.model
    def _default_operating_unit(self):
        team = self.env['crm.team']._get_default_team_id()
        if team.operating_unit_id:
            return team.operating_unit_id
        return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=_default_operating_unit,
    )

    @api.onchange('crm_team_id')
    def onchange_team_id(self):
        if self.crm_team_id:
            self.operating_unit_id = self.crm_team_id.operating_unit_id

    @api.onchange('operating_unit_id')
    def onchange_operating_unit_id(self):
        if self.crm_team_id and self.crm_team_id.operating_unit_id != \
                self.operating_unit_id:
            self.crm_team_id = False

    @api.multi
    @api.constrains('crm_team_id', 'operating_unit_id')
    def _check_team_operating_unit(self):
        for rec in self:
            if (rec.crm_team_id and
                    rec.crm_team_id.operating_unit_id != rec.operating_unit_id):
                raise ValidationError(_('Configuration error. The Operating '
                                        'Unit of the sales team must match '
                                        'with that of the POS Config.'))

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise ValidationError(_('Configuration error. The Company in '
                                        'the POS Config and in the Operating '
                                        'Unit must be the same.'))


