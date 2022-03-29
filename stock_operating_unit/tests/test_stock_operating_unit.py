# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.addons.stock.tests import common


class TestStockOperatingUnit(common.TestStockCommon):
    def setUp(self):
        super(TestStockOperatingUnit, self).setUp()
        self.ResUsers = self.env["res.users"]
        self.WarehouseObj = self.env["stock.warehouse"]
        self.LocationObj = self.env["stock.location"]
        # company
        self.company1 = self.env.ref("base.main_company")
        # groups
        self.group_stock_manager = self.env.ref("stock.group_stock_manager")
        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c = self.env.ref("operating_unit.b2c_operating_unit")
        # Products
        self.product1 = self.env.ref("product.product_product_7")
        self.product2 = self.env.ref("product.product_product_9")
        self.product3 = self.env.ref("product.product_product_11")
        # Locations
        b2c_wh = self.env.ref("stock_operating_unit.stock_warehouse_b2c")
        b2c_wh.lot_stock_id.write({"operating_unit_id": self.b2c.id})
        self.location_b2c_id = b2c_wh.lot_stock_id.id
        self.b2c_type_in_id = b2c_wh.in_type_id.id
        self.b2c_type_int_id = b2c_wh.int_type_id.id
        # Create users
        self.user1_id = self._create_user(
            "stock_user_1",
            [self.group_stock_manager],
            self.company1,
            [self.ou1, self.b2c],
        )
        self.user2_id = self._create_user(
            "stock_user_2", [self.group_stock_manager], self.company1, [self.b2c]
        )
        # Create Incoming Shipments
        self.picking_in1 = self._create_picking(
            self.user1_id,
            self.b2c.id,
            self.b2c_type_in_id,
            self.supplier_location,
            self.stock_location,
        )
        self.picking_in2 = self._create_picking(
            self.user2_id,
            self.b2c.id,
            self.b2c_type_in_id,
            self.supplier_location,
            self.location_b2c_id,
        )
        # Create Internal Shipment
        self.picking_int = self._create_picking(
            self.user1_id,
            self.b2c.id,
            self.b2c_type_int_id,
            self.stock_location,
            self.location_b2c_id,
        )

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.ResUsers.with_context(**{"no_reset_password": True}).create(
            {
                "name": "Stock User",
                "login": login,
                "password": "demo",
                "email": "chicago@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user.id

    def _create_picking(self, user_id, ou_id, picking_type, src_loc_id, dest_loc_id):
        """Create a Picking."""
        picking = self.PickingObj.with_user(user_id).create(
            {
                "picking_type_id": picking_type,
                "location_id": src_loc_id,
                "location_dest_id": dest_loc_id,
                "operating_unit_id": ou_id,
            }
        )
        self.MoveObj.with_user(user_id).create(
            {
                "name": "a move",
                "product_id": self.productA.id,
                "product_uom_qty": 3.0,
                "product_uom": self.productA.uom_id.id,
                "picking_id": picking.id,
                "location_id": src_loc_id,
                "location_dest_id": dest_loc_id,
            }
        )
        return picking
