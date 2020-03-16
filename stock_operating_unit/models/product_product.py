# Copyright (c) 2020 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_domain_locations(self):
        domain = super(ProductProduct, self)._get_domain_locations()
        ou_ids = self.env.user.operating_unit_ids.ids
        return (
            domain[0] + ['|',
                         ('location_id.operating_unit_id', 'in', ou_ids),
                         ('location_id.operating_unit_id', '=', False)],
            domain[1] + ['|',
                         ('location_dest_id.operating_unit_id', 'in', ou_ids),
                         ('location_dest_id.operating_unit_id', '=', False)],
            domain[2] + ['|',
                         ('location_id.operating_unit_id', 'in', ou_ids),
                         ('location_id.operating_unit_id', '=', False)])
