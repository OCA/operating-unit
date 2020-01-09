# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(
        self, product_id, product_qty, product_uom, origin, values, partner
    ):
        res = super(StockRule, self)._prepare_purchase_order(
            product_id, product_qty, product_uom, origin, values, partner
        )
        res["operating_unit_id"] = values["warehouse_id"].operating_unit_id.id
        return res

    def _make_po_get_domain(self, values, partner):
        res = super(StockRule, self)._make_po_get_domain(values, partner)
        res += (("operating_unit_id", "=", values.get(
            "operating_unit_id", False)),)
        return res
