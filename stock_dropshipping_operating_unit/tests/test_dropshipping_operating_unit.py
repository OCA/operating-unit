# Copyright 2026 Luc De Meyer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.models import Command

from odoo.addons.sale_stock_operating_unit.tests.test_sale_stock_operating_unit import (
    TestSaleStockOperatingUnit,
)


class TestDropshippingOperatingUnit(TestSaleStockOperatingUnit):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dropship_route = cls.env.ref("stock_dropshipping.route_drop_shipping")
        cls.dropship_product = cls.env.ref("product.product_product_7")
        cls.dropship_product.write(
            {
                "type": "consu",
                "is_storable": True,
                "route_ids": [Command.link(cls.dropship_route.id)],
            }
        )
        cls.dropship_product.product_tmpl_id.write(
            {
                "seller_ids": [
                    Command.create(
                        {
                            "partner_id": cls.env.ref("base.res_partner_1").id,
                            "price": 100.0,
                        }
                    )
                ],
            }
        )

    def _create_dropship_sale_order(self, uid, ou):
        sale = (
            self.env["sale.order"]
            .with_user(uid)
            .create(
                {
                    "partner_id": self.customer.id,
                    "partner_invoice_id": self.customer.id,
                    "partner_shipping_id": self.customer.id,
                    "pricelist_id": self.pricelist.id,
                    "operating_unit_id": ou.id,
                }
            )
        )
        self.env["sale.order.line"].with_user(uid).create(
            {
                "order_id": sale.id,
                "product_id": self.dropship_product.id,
                "name": "Drop-ship line",
                "price_unit": 150.0,
            }
        )
        return sale

    def test_dropship_ou_propagation(self):
        """
        Confirming a dropship SO propagates its OU to the generated PO.
        """
        sale = self._create_dropship_sale_order(self.user1.id, self.ou1)
        sale.action_confirm()
        po = sale.order_line.purchase_line_ids.order_id
        self.assertEqual(
            po.operating_unit_id,
            self.ou1,
            "PO operating_unit_id should match the SO's OU",
        )
        self.assertEqual(
            po.requesting_operating_unit_id,
            self.ou1,
            "PO requesting_operating_unit_id should match the SO's OU",
        )
