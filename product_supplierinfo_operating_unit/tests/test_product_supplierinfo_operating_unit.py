# Copyright 2021 Rujia Liu
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProductSupplierinfoOperatingUnit(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env.ref("product_supplierinfo_operating_unit.test_product")
        self.warehouse = self.env.ref("stock.warehouse0")
        self.env.ref("stock.route_warehouse0_mto").active = True
        self.warehouse_b2b = self.env.ref("stock_operating_unit.stock_warehouse_b2b")
        self.main_ou = self.env.ref("operating_unit.main_operating_unit")
        self.b2b_ou = self.env.ref("operating_unit.b2b_operating_unit")

    def _create_sale_order(self, warehouse):
        with Form(self.env["sale.order"]) as so:
            so.partner_id = self.env.ref("base.res_partner_12")
            so.warehouse_id = warehouse
            with so.order_line.new() as line:
                line.product_id = self.product
                line.product_uom_qty = 20
        return so.save()

    def test_prepare_purchase_order(self):
        # this function is more about integration testing
        self.assertTrue(
            len(self.product.seller_ids) == 3,
            "There should be 3 vendor pricelists for this product loaded from demo",
        )

        # _prepare_purchase_order should use main operating unit
        sale_order_1 = self._create_sale_order(self.warehouse)
        sale_order_1.action_confirm()
        purchase_order = self.env["purchase.order"].search(
            [("origin", "ilike", str(sale_order_1.name))]
        )
        self.assertTrue(purchase_order)
        self.assertEqual(purchase_order.operating_unit_id, self.main_ou)
        self.assertEqual(purchase_order.requesting_operating_unit_id, self.main_ou)
        # check the seller consistent:
        # pick the seller who has cheapest price regardless OU
        self.assertEqual(purchase_order.partner_id, self.env.ref("base.res_partner_1"))

        # _prepare_purchase_order should use b2b operating unit
        sale_order_2 = self._create_sale_order(self.warehouse_b2b)
        sale_order_2.action_confirm()
        purchase_order = self.env["purchase.order"].search(
            [("origin", "ilike", str(sale_order_2.name))]
        )
        self.assertTrue(purchase_order)
        self.assertEqual(purchase_order.operating_unit_id, self.b2b_ou)
        self.assertEqual(purchase_order.requesting_operating_unit_id, self.b2b_ou)
        # check the seller consistent:
        # pick the seller who has cheapest price regardless OU
        self.assertEqual(purchase_order.partner_id, self.env.ref("base.res_partner_1"))

    def test_prepare_sellers(self):
        # this function is more about integration testing
        # 1. test no OU in ctx: should pick any seller who has cheapest price
        #    regardless its OU
        self.assertTrue(
            len(self.product.seller_ids) == 3,
            "There should be 3 vendor pricelists for this product loaded from demo",
        )

        sale_order_no_ctx = self._create_sale_order(self.warehouse_b2b)
        sale_order_no_ctx.action_confirm()
        purchase_order = self.env["purchase.order"].search(
            [("origin", "ilike", str(sale_order_no_ctx.name))]
        )
        self.assertTrue(purchase_order)
        # check the seller consistent:
        # pick the seller who has cheapest price regardless OU
        self.assertEqual(purchase_order.partner_id, self.env.ref("base.res_partner_1"))

        # 2. test b2b OU in ctx: should pick any seller who either belongs to b2b
        #    or doesn't have a OU and has the cheapest price
        supplierinfo = self.env.ref(
            "product_supplierinfo_operating_unit.product_supplierinfo_ou_1"
        )
        supplierinfo.price = 550

        sale_order_with_ctx = self._create_sale_order(self.warehouse_b2b)
        sale_order_with_ctx.with_context(
            {"operating_unit_id": self.b2b_ou.id}
        ).action_confirm()
        purchase_order = self.env["purchase.order"].search(
            [("origin", "ilike", str(sale_order_with_ctx.name))]
        )
        self.assertTrue(purchase_order)
        # #check the seller consistant
        # pick the seller who has cheapest price and doesn't belong to main OU
        self.assertEqual(purchase_order.partner_id, self.env.ref("base.res_partner_2"))

        supplierinfo_no_ou = self.env.ref(
            "product_supplierinfo_operating_unit.product_supplierinfo_ou_3"
        )
        supplierinfo_no_ou.price = 550
        sale_order_with_ctx = self._create_sale_order(self.warehouse_b2b)
        sale_order_with_ctx.with_context(
            {"operating_unit_id": self.b2b_ou.id}
        ).action_confirm()
        purchase_order = self.env["purchase.order"].search(
            [("origin", "ilike", str(sale_order_with_ctx.name))]
        )
        self.assertTrue(purchase_order)
        # #check the seller consistant
        # pick the seller who doesn't belong to any OU because it now has cheapest price
        self.assertEqual(purchase_order.partner_id, self.env.ref("base.res_partner_3"))
