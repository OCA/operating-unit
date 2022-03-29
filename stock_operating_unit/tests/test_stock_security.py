# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import tagged

from . import test_stock_operating_unit as test_stock_ou


@tagged("post_install", "-at_install")
class TestStockPicking(test_stock_ou.TestStockOperatingUnit):
    def test_stock_ou_security(self):
        """Test Security of Stock Operating Unit"""
        # User 1 can list the warehouses assigned to
        # Main and B2C OU
        wh_ids = (
            self.WarehouseObj.with_user(self.user1_id)
            .search([("operating_unit_id", "in", [self.ou1.id, self.b2c.id])])
            .ids
        )
        self.assertNotEqual(
            wh_ids,
            [],
            "User does not have access to"
            "Warehouses which belong to Main and B2C"
            "Operating Unit.",
        )
        # User 1 can list the locations assigned to Main and b2c OU
        location_ids = (
            self.LocationObj.with_user(self.user1_id)
            .search([("operating_unit_id", "in", [self.ou1.id, self.b2c.id])])
            .ids
        )
        self.assertNotEqual(
            location_ids,
            [],
            "User does not have access to"
            "Locations which belong to Main and B2C"
            "Operating Unit.",
        )
        # User 2 cannot list the warehouses assigned to Main OU
        wh_ids = (
            self.WarehouseObj.with_user(self.user2_id)
            .search([("operating_unit_id", "=", self.ou1.id)])
            .ids
        )
        self.assertEqual(
            wh_ids,
            [],
            "User 2 should not be able to list"
            "the warehouses assigned to Main Operating Unit.",
        )
        # User 2 cannot list the locations assigned to Main OU
        location_ids = (
            self.LocationObj.with_user(self.user2_id)
            .search([("operating_unit_id", "in", [self.ou1.id])])
            .ids
        )
        self.assertEqual(
            location_ids,
            [],
            "User 2 should not be able to list" "the locations assigned to Main OU.",
        )
        pickings = [self.picking_in1.id, self.picking_in2.id, self.picking_int.id]
        # User 1 can list the pickings 1, 2, 3
        picking_ids = (
            self.PickingObj.with_user(self.user1_id)
            .search([("id", "in", pickings)])
            .ids
        )
        self.assertNotEqual(
            picking_ids,
            [],
            "User 1 cannot list the" "pickings assigned to pickings 1, 2, 3.",
        )
        # User 1 can list the stock moves assigned to pickings 1, 2, 3
        move_ids = (
            self.MoveObj.with_user(self.user1_id)
            .search([("picking_id", "in", pickings)])
            .ids
        )
        self.assertNotEqual(
            move_ids,
            [],
            "User 1 cannot list the" "stock moves assigned to pickings 1, 2, 3.",
        )
        # User 2 cannot list the the stock moves assigned to picking 1
        move_ids = (
            self.MoveObj.with_user(self.user2_id)
            .search([("picking_id", "=", self.picking_in1.id)])
            .ids
        )
        self.assertEqual(
            move_ids,
            [],
            "User 2 should not be able to list the "
            "stock moves assigned to picking 1.",
        )
        # User 2 can list the picking 1
        picking_ids = (
            self.PickingObj.with_user(self.user2_id)
            .search([("id", "=", self.picking_in1.id)])
            .ids
        )
        self.assertEqual(
            len(picking_ids), 1, "User 2 should be able to list" "the picking 1."
        )
