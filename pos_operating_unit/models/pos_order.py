# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        related='config_id.operating_unit_id',
        store=True         
    )

    crm_team_id = fields.Many2one(
        comodel_name='crm.team', 
        related='config_id.crm_team_id', 
        string="Sales Team", 
        )

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a pos order.
        """
        res = super(PosOrder, self)._prepare_invoice()
        res.update( {
            'operating_unit_id': self.config_id.operating_unit_id.id or False,
        })
        return res


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    operating_unit_id = fields.Many2one(related='order_id.operating_unit_id',
                                        string='Operating Unit',
                                        store=True)
