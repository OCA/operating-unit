# Copyright 2015-TODAY Eficent
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# Copyright 2019 XOE Corp. SAS (David Arnold)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def operating_unit_default_get(self):
        """ Returns a single operating unit for a given user. Use for
        transactional data that belongs to only one operating unit.
        """
        return self.current_operating_unit_id

    @api.model
    def operating_units_default_get(self):
        """ Returns a set of operating units for a given user. Use for
        metadata data that possibly belongs to several operating units.
        """

        # TODO: Implement when Odoo's company multi selection
        # implementation becomes known.
        # see: https://git.io/fjc25, notably: https://git.io/fjc29
        return self.current_operating_unit_id

    allowed_operating_unit_ids = fields.Many2many(
        'operating.unit', 'operating_unit_users_rel', 'user_id', 'operating_unit_id',
        'Allowed Operating Units'
    )
    current_operating_unit_id = fields.Many2one(
        'operating.unit', 'Current Operating Unit',
        domain="[('id', 'in', allowed_operating_unit_ids)]"
    )
