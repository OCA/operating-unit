# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    operating_unit_id = fields.Many2one(
        'operating.unit',
        'Requesting Operating Unit',
        readonly=True,
        states={'draft': [('readonly', False)]})

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        res = super(StockPicking, self).onchange_picking_type()
        if self.picking_type_id:
            unit = self.picking_type_id.warehouse_id.operating_unit_id
            self.operating_unit_id = unit
        return res

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise UserError(
                    _('Configuration error. The Company in the Stock Picking '
                      'and in the Operating Unit must be the same.')
                )

    @api.multi
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_picking_type_operating_unit(self):
        for rec in self:
            warehouse = rec.picking_type_id.warehouse_id
            if (rec.picking_type_id and rec.operating_unit_id and
                    warehouse.operating_unit_id != rec.operating_unit_id):
                raise UserError(
                    _('Configuration error. The Operating Unit of the picking '
                      'must be the same as that of the warehouse of the '
                      'Picking Type.')
                )
