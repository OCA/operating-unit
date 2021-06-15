# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from datetime import datetime

from odoo.exceptions import ValidationError
from odoo.tests import common
from odoo.tests.common import Form


class TestMrpOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestMrpOperatingUnit, self).setUp()
        self.res_users_model = self.env["res.users"]
        self.mrp_production_model = self.env["mrp.production"]
        self.company = self.env.ref("base.main_company")
        self.bom_id = self.env.ref("mrp.mrp_bom_manufacture")

        # Products
        self.product1 = self.env.ref("product.product_product_4c")
        # Stock Location
        self.stock_location = self.env.ref("stock.stock_location_shop0")

        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")
        # Chicago Operating Unit
        self.chicago = self.env.ref("stock_operating_unit.operating_unit_shop0")
        # Groups
        self.grp_mrp_saleman = self.env.ref("sales_team.group_sale_salesman")
        self.grp_mrp_manager = self.env.ref("mrp.group_mrp_manager")

        # Users
        self.user1 = self._create_user(
            "user_1", [self.grp_mrp_saleman], self.company, [self.ou1, self.chicago]
        )
        self.user2 = self._create_user(
            "user_2",
            [self.grp_mrp_saleman, self.grp_mrp_manager],
            self.company,
            [self.chicago],
        )

        # Manufacturing Orders
        self.mrp_record1 = self._create_mrp("Manufacturing Order 1", self.ou1)
        self.mrp_record2 = self._create_mrp(
            "Manufacturing Order 2", self.chicago, self.stock_location
        )

    def _create_user(self, login, groups, company, operating_units, context=None):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create(
            {
                "name": "Test HR Contrac User",
                "login": login,
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    def _create_mrp(self, name, operating_unit, stock_location=False):
        if operating_unit == self.ou1:
            mrp = self.mrp_production_model.create(
                {
                    "name": name,
                    "product_id": self.product1.id,
                    "bom_id": self.bom_id.id,
                    "product_qty": "10.0",
                    "product_uom_id": self.product1.uom_id.id,
                    "operating_unit_id": operating_unit.id,
                }
            )
        else:
            mrp = self.mrp_production_model.create(
                {
                    "name": name,
                    "product_id": self.product1.id,
                    "bom_id": self.bom_id.id,
                    "product_qty": "10.0",
                    "product_uom_id": self.product1.uom_id.id,
                    "operating_unit_id": operating_unit.id,
                    "location_src_id": stock_location.id,
                    "location_dest_id": stock_location.id,
                }
            )
        return mrp

    def test_check_location_operating_unit(self):
        with self.assertRaises(ValidationError):
            self.mrp_record1.location_src_id = self.stock_location.id

        with self.assertRaises(ValidationError):
            self.mrp_record2.operating_unit_id = False

    def test_onchange_operating_unit_id(self):
        # Test the ou does not belong to any warehouse
        test_ou = self.env["operating.unit"].create(
            {
                "name": "Test OU",
                "code": "TOU",
                "partner_id": self.env.ref("stock.res_partner_company_1").id,
                "company_id": self.env.ref("stock.res_company_1").id,
            }
        )
        location_test = self.env["stock.location"].create(
            {
                "name": "Test Location",
                "usage": "internal",
                "operating_unit_id": test_ou.id,
                "company_id": self.env.ref("stock.res_company_1").id,
            }
        )
        record = self._create_mrp(
            "Test Onchange Operating Unit", test_ou, location_test
        )
        self.assertEqual(None, record._onchange_operating_unit_id())

        # Test onchange picking_type_id
        new_picking_type_id = self.env["stock.picking.type"].search(
            [
                ("company_id", "=", self.mrp_record1.company_id.id),
                ("code", "=", "mrp_operation"),
                ("warehouse_id.operating_unit_id", "=", self.b2b.id),
            ]
        )
        with Form(self.mrp_record1) as mrp_form:
            mrp_form.operating_unit_id = self.b2b
            self.assertEqual(new_picking_type_id, mrp_form.picking_type_id)

    def test_mrp_ou(self):
        record = self.mrp_production_model.with_user(self.user2.id).search(
            [("id", "=", self.mrp_record1.id), ("operating_unit_id", "=", self.ou1.id)]
        )
        self.assertEqual(
            record.ids,
            [],
            "User 2 should not have access to " "OU : %s" % self.ou1.name,
        )

        with self.assertRaises(ValidationError):
            self.mrp_record1.operating_unit_id = False
        with self.assertRaises(ValidationError):
            self.mrp_record1.write({"operating_unit_id": self.chicago.id})

    def test_prepare_mo_vals(self):
        self.assertIn(
            "operating_unit_id",
            self.env["stock.rule"]._prepare_mo_vals(
                self.env.ref("product.product_product_4"),
                0,
                self.env.ref("uom.product_uom_unit"),
                self.env.ref("stock.stock_location_shop0"),
                "test",
                False,
                self.env.company,
                {
                    "date_planned": datetime.today(),
                    "warehouse_id": self.env.ref("stock.warehouse0"),
                },
                self.env.ref("mrp.mrp_bom_manufacture"),
            ),
        )
