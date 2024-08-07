# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from odoo.addons.sale_operating_unit.tests.test_sale_operating_unit import (
    TestSaleOperatingUnit,
)
from odoo.addons.stock_operating_unit.tests.test_stock_operating_unit import (
    TestStockOperatingUnit,
)


class TestSaleStockOperatingUnit(TestStockOperatingUnit, TestSaleOperatingUnit):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Products
        cls.stored_product = cls.env.ref("stock.product_cable_management_box")
        cls.stored_product.write({"invoice_policy": "order"})

        cls.sale3 = cls._create_sale_order(
            cls.user1.id,
            cls.customer,
            cls.stored_product,
            cls.pricelist,
            cls.sale_team_ou1,
        )
        cls.sale4 = cls._create_sale_order(
            cls.user2.id,
            cls.customer,
            cls.stored_product,
            cls.pricelist,
            cls.sale_team_b2c,
        )

    def test_security(self):
        """Test Sale Operating Unit"""
        # Confirm Sale1
        self._confirm_sale(self.sale3)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(
            self.sale3.operating_unit_id,
            self.sale3.picking_ids.operating_unit_id,
            "OU in Sale Order and Picking should be same",
        )
        # Confirm Sale2
        self._confirm_sale(self.sale4)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(
            self.sale4.operating_unit_id,
            self.sale4.picking_ids.operating_unit_id,
            "OU in Sale Order and Picking should be same",
        )
