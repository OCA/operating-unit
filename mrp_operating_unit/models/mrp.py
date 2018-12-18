# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit',
        readonly=True,
        states={'confirmed': [('readonly', False)]},
        default=lambda self: self.env['res.users'
                                      ].operating_unit_default_get(self._uid)
    )

    @api.constrains('operating_unit_id', 'location_src_id', 'location_dest_id')
    def _check_location_operating_unit(self):
        for mo in self:
            if (
                not mo.operating_unit_id and
                (mo.location_src_id.operating_unit_id or
                 mo.location_dest_id.operating_unit_id)
            ):
                raise ValidationError(_(
                    'The Operating Unit of the Manufacturing Order must match '
                    'with that of the Raw Materials and Finished Product '
                    'Locations.'))
            if (
                mo.operating_unit_id and
                mo.operating_unit_id != mo.location_src_id.operating_unit_id
            ):
                raise ValidationError(_(
                    'The Operating Unit of the Manufacturing Order must match '
                    'with that of the Raw Materials and Finished Product '
                    'Locations.'))
            if (
                mo.operating_unit_id and
                mo.operating_unit_id != mo.location_dest_id.operating_unit_id
            ):
                raise ValidationError(_(
                    'The Operating Unit of the Manufacturing Order must match '
                    'with that of the Raw Materials and Finished Product '
                    'Locations.'))
        return True
