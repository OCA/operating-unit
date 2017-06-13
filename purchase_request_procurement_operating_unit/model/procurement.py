# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import models, api, _


class Procurement(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def _prepare_purchase_request(self, procurement):
        res = super(Procurement, self)._prepare_purchase_request(procurement)
        if procurement.location_id.operating_unit_id:
            res.update({
                'operating_unit_id':
                    procurement.location_id.operating_unit_id.id
            })
        return res

    @api.multi
    @api.constrains('location_id', 'request_id')
    def _check_purchase_request_operating_unit(self):
        for rec in self:
            if rec.request_id and rec.location_id.operating_unit_id and \
                    rec.request_id.operating_unit_id != \
                    rec.location_id.operating_unit_id:
                raise Warning(_('The Purchase Request and the Procurement '
                                'Order must belong to the same Operating'
                                'Unit.'))

    @api.multi
    @api.constrains('location_id', 'warehouse_id')
    def _check_warehouse_operating_unit(self):
        for rec in self:
            if rec.warehouse_id and rec.location_id.operating_unit_id and \
                    rec.warehouse_id.operating_unit_id != \
                    rec.location_id.operating_unit_id:
                raise Warning(_('Warehouse and location of procurement order '
                                'must belong to the same Operating Unit.'))
