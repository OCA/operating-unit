# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, api, _
from odoo.exceptions import ValidationError


class Procurement(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def _prepare_purchase_request(self):
        res = super(Procurement, self)._prepare_purchase_request()
        if self.location_id.operating_unit_id:
            res.update({
                'operating_unit_id': self.location_id.operating_unit_id.id
            })
        return res

    @api.multi
    @api.constrains('location_id', 'request_id')
    def _check_purchase_request_operating_unit(self):
        for procurement in self:
            if procurement.request_id and\
                    procurement.location_id.operating_unit_id and\
                    procurement.request_id.operating_unit_id !=\
                    procurement.location_id.operating_unit_id:
                raise ValidationError(_('The Purchase Request and the '
                                        'Procurement Order must belong to '
                                        'the same Operating Unit.'))

    @api.multi
    @api.constrains('location_id', 'warehouse_id')
    def _check_warehouse_operating_unit(self):
        for procurement in self:
            if procurement.warehouse_id and\
                    procurement.location_id.operating_unit_id and \
                    procurement.warehouse_id.operating_unit_id != \
                    procurement.location_id.operating_unit_id:
                raise ValidationError(_('Warehouse and location of '
                                        'procurement  order must belong to '
                                        'the same Operating Unit.'))
