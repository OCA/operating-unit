# -*- coding: utf-8 -*-
# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=lambda self: (self.env['res.users'].
                              operating_unit_default_get(self.env.uid))
    )
