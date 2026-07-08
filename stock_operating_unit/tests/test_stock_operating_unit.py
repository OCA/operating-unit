# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.fields import Command

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon
from odoo.addons.stock.tests import common


class TestStockOperatingUnit(common.TestStockCommon, OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResUsers = cls.env["res.users"]
        cls.WarehouseObj = cls.env["stock.warehouse"]
        cls.LocationObj = cls.env["stock.location"]
        # groups
        cls.group_stock_manager = cls.env.ref("stock.group_stock_manager")
        # Products
        cls.product1 = cls.env["product.product"].create(
            {
                "name": "Storage Box Test",
                "standard_price": 14.0,
                "list_price": 15.8,
                "type": "consu",
            }
        )
        cls.product2 = cls.env["product.product"].create(
            {
                "name": "Pedal Bin Test",
                "standard_price": 10.0,
                "list_price": 47.0,
                "type": "consu",
            }
        )
        cls.product3 = cls.env["product.product"].create(
            {
                "name": "Conference Chair Test",
                "standard_price": 28.0,
                "list_price": 33.0,
                "type": "consu",
            }
        )
        # Locations
        cls.b2c_wh = cls.env["stock.warehouse"].create(
            {
                "name": "B2C Warehouse Test",
                "code": "B2C_Test",
                "partner_id": cls.partner.id,
                "company_id": cls.company.id,
                "operating_unit_id": cls.b2c.id,
            }
        )
        cls.b2c_wh.lot_stock_id.write({"operating_unit_id": cls.b2c.id})
        cls.location_b2c_id = cls.b2c_wh.lot_stock_id.id
        cls.b2c_type_in_id = cls.b2c_wh.in_type_id.id
        cls.b2c_type_int_id = cls.b2c_wh.int_type_id.id
        # Update users
        cls.user1.write(
            {
                "group_ids": [
                    Command.link(cls.group_stock_manager.id),
                ],
                "operating_unit_ids": [
                    Command.link(cls.ou1.id),
                    Command.link(cls.b2c.id),
                ],
            }
        )
        cls.user2.write(
            {
                "group_ids": [
                    Command.link(cls.group_stock_manager.id),
                ],
                "operating_unit_ids": [
                    Command.set(cls.b2c.id),
                ],
            }
        )
        # Create Incoming Shipments
        cls.picking_in1 = cls._create_picking(
            cls.user1,
            cls.b2c.id,
            cls.b2c_type_in_id,
            cls.supplier_location.id,
            cls.stock_location.id,
        )
        cls.picking_in2 = cls._create_picking(
            cls.user2,
            cls.b2c.id,
            cls.b2c_type_in_id,
            cls.supplier_location.id,
            cls.location_b2c_id,
        )
        # Create Internal Shipment
        cls.picking_int = cls._create_picking(
            cls.user1,
            cls.b2c.id,
            cls.b2c_type_int_id,
            cls.stock_location.id,
            cls.location_b2c_id,
        )

    @classmethod
    def _create_picking(cls, user_id, ou_id, picking_type, src_loc_id, dest_loc_id):
        """Create a Picking."""
        picking = cls.PickingObj.with_user(user_id).create(
            {
                "picking_type_id": picking_type,
                "location_id": src_loc_id,
                "location_dest_id": dest_loc_id,
                "operating_unit_id": ou_id,
            }
        )
        cls.MoveObj.with_user(user_id).create(
            {
                "product_id": cls.productA.id,
                "product_uom_qty": 3.0,
                "product_uom": cls.productA.uom_id.id,
                "picking_id": picking.id,
                "location_id": src_loc_id,
                "location_dest_id": dest_loc_id,
            }
        )
        return picking
