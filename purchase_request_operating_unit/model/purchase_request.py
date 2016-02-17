# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=lambda self:
        self.env['res.users'].
        operating_unit_default_get(self._uid),
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and \
                    rec.company_id != rec.operating_unit_id.company_id:
                raise Warning(_("The Company in the Purchase Request and in "
                                "the Operating Unit must be the same."))

    @api.multi
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_warehouse_operating_unit(self):
        for rec in self:
            picking_type = rec.picking_type_id
            if picking_type:
                if picking_type.warehouse_id and\
                        picking_type.warehouse_id.operating_unit_id\
                        and rec.operating_unit_id and\
                        picking_type.warehouse_id.operating_unit_id !=\
                        rec.operating_unit_id:
                    raise Warning(_("Configuration error! The Purchase Request"
                                    " and the Warehouse of picking type must"
                                    " belong to the same Operating Unit."))


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    operating_unit_id = fields.Many2one(
        'operating.unit',
        related='request_id.operating_unit_id',
        string='Operating Unit', readonly=True,
        store=True,
    )
