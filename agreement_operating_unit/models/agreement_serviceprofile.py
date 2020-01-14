# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AgreementServiceprofile(models.Model):
    _inherit = 'agreement.serviceprofile'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        related='agreement_id.operating_unit_id',
        string='Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get(
            self._uid)
    )
