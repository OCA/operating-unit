# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    @api.constrains('purchase_line_id', 'location_id')
    def _check_purchase_order_operating_unit(self):
        for proc in self:
            if not proc.purchase_line_id:
                continue
            ou = proc.location_id.operating_unit_id
            order_ou = proc.purchase_line_id.operating_unit_id
            if (ou != order_ou and
                    proc.location_id.usage not in ('supplier', 'customer')):
                raise ValidationError(
                    _('Configuration error. The Quotation / Purchase Order '
                      'and the Procurement Order must belong to the same '
                      'Operating Unit.')
                    )

    @api.multi
    def _prepare_purchase_order(self, partner):
        res = super(ProcurementOrder, self)._prepare_purchase_order(partner)
        operating_unit = self.location_id.operating_unit_id
        if operating_unit:
            res.update({
                'operating_unit_id': operating_unit.id,
                'requesting_operating_unit_id': operating_unit.id
            })
        return res
