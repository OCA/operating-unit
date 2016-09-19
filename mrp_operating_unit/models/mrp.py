# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))

    @api.constrains('operating_unit_id', 'location_src_id', 'location_dest_id')
    def _check_location_operating_unit(self):
        for mo in self:
            if (
                not mo.operating_unit_id and
                (mo.location_src_id.operating_unit_id or
                 mo.location_dest_id.operating_unit_id)
            ):
                raise Warning(_('The Operating Unit of the Manufacturing Order\
                                 must match with that of the Raw Materials and\
                                  Finished Product Locations.'))
            if (
                mo.operating_unit_id and
                mo.operating_unit_id != mo.location_src_id.operating_unit_id
            ):
                raise Warning(_('The Operating Unit of the Manufacturing Order\
                                 must match with that of the Raw Materials and\
                                  Finished Product Locations.'))
            if (
                mo.operating_unit_id and
                mo.operating_unit_id != mo.location_dest_id.operating_unit_id
            ):
                raise Warning(_('The Operating Unit of the Manufacturing Order\
                                 must match with that of the Raw Materials and\
                                  Finished Product Locations.'))
        return True
