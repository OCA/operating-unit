# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


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
                raise ValidationError(_(
                    'The Production Order and the Procurement Order must '
                    'belong to the same Operating Unit.'))
        return True

    @api.model
    def _prepare_mo_vals(self, bom):
        res = super(ProcurementOrder, self)._prepare_mo_vals(bom)
        if self.location_id.operating_unit_id:
            res['operating_unit_id'] = self.location_id.operating_unit_id.id
        return res
