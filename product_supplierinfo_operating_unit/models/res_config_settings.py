# Copyright 2017 Open For Small Business Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_manage_vendor_ou_price = fields.Boolean(
        string="Operating Unit Vendor Pricing",
        implied_group="product_supplierinfo_operating_unit.group_manage_vendor_ou_price",
    )
