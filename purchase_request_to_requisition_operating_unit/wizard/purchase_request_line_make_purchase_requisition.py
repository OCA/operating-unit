# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseRequestLineMakePurchaseRequisition(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.requisition"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        readonly=True,
    )

    @api.model
    def default_get(self, fields):
        res = super(PurchaseRequestLineMakePurchaseRequisition, self).\
            default_get(fields)
        request_line_obj = self.env['purchase.request.line']
        request_line_ids = self._context.get('active_ids', [])
        operating_unit_id = False
        for line in request_line_obj.browse(request_line_ids):
            line_operating_unit_id = line.request_id.operating_unit_id \
                and line.request_id.operating_unit_id.id or False
            if operating_unit_id\
                    and line_operating_unit_id != operating_unit_id:
                raise ValidationError(_('Could not process !'
                                        'You have to select lines from'
                                        'the same operating unit.'))
            else:
                operating_unit_id = line_operating_unit_id
        res['operating_unit_id'] = operating_unit_id
        return res

    @api.model
    def _prepare_purchase_requisition(self, picking_type_id,
                                      company_id):
        res = super(PurchaseRequestLineMakePurchaseRequisition, self).\
            _prepare_purchase_requisition(picking_type_id, company_id)
        if self.operating_unit_id:
            res.update({'operating_unit_id': self.operating_unit_id.id})
        return res
