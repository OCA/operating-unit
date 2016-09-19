# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning


class ProcurementOrder(models.Model):

    _inherit = 'procurement.order'

    @api.constrains('location_id', 'production_id')
    def _check_mrp_production_operating_unit(self):
        for pr in self:
            if (
                pr.production_id and
                pr.location_id.operating_unit_id and
                pr.production_id.operating_unit_id !=
                    pr.location_id.operating_unit_id
            ):
                raise Warning(_('The Production Order and the Procurement\
                 Order must belong to the same Operating Unit.'))
        return True

    @api.model
    def _prepare_mo_vals(self, procurement):
        res = super(ProcurementOrder, self)._prepare_mo_vals(procurement)
        if procurement.location_id.operating_unit_id:
            res['operating_unit_id'] = \
                procurement.location_id.operating_unit_id.id
        return res
