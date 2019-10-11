# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.stock.tests import common
from odoo.addons.operating_unit.tests.OperatingUnitsTransactionCase import \
    OperatingUnitsTransactionCase


class TestStockOperatingUnit(common.TestStockCommon,
                             OperatingUnitsTransactionCase):

    def setUp(self):
        super(TestStockOperatingUnit, self).setUp()
        self.ResUsers = self.env['res.users']
        self.WarehouseObj = self.env['stock.warehouse']
        self.LocationObj = self.env['stock.location']
        # company
        self.company1 = self.env.ref('base.main_company')
        # groups
        self.group_stock_manager = self.env.ref('stock.group_stock_manager')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Products
        self.product1 = self.env.ref('product.product_product_7')
        # Locations
        b2c_wh = self.env.ref('stock_operating_unit.stock_warehouse_b2c')
        b2c_wh.lot_stock_id.write({'operating_unit_id': self.b2c.id})
        self.location_b2c_id = b2c_wh.lot_stock_id.id
        self.b2c_type_in_id = b2c_wh.in_type_id.id
        self.b2c_type_int_id = b2c_wh.int_type_id.id
        # Create users
        self.user1_id = self._create_user('stock_user_1',
                                          [self.group_stock_manager],
                                          self.company1,
                                          [self.ou1, self.b2c]).id
        self.user2_id = self._create_user('stock_user_2',
                                          [self.group_stock_manager],
                                          self.company1,
                                          [self.b2c]).id
        # Create Incoming Shipments
        self.picking_in1 = self._create_picking(self.user1_id,
                                                self.b2c.id,
                                                self.b2c_type_in_id,
                                                self.supplier_location,
                                                self.stock_location)
        self.picking_in2 = self._create_picking(self.user2_id,
                                                self.b2c.id,
                                                self.b2c_type_in_id,
                                                self.supplier_location,
                                                self.location_b2c_id)
        # Create Internal Shipment
        self.picking_int = self._create_picking(self.user1_id,
                                                self.b2c.id,
                                                self.b2c_type_int_id,
                                                self.stock_location,
                                                self.location_b2c_id)

    def _create_picking(self, user_id, ou_id, picking_type, src_loc_id,
                        dest_loc_id):
        """Create a Picking."""
        picking = self.PickingObj.sudo(user_id).create({
            'picking_type_id': picking_type,
            'location_id': src_loc_id,
            'location_dest_id': dest_loc_id,
            'operating_unit_id': ou_id,
        })
        self.MoveObj.sudo(user_id).create({
            'name': 'a move',
            'product_id': self.product1.id,
            'product_uom_qty': 3.0,
            'product_uom': self.product1.uom_id.id,
            'picking_id': picking.id,
            'location_id': src_loc_id,
            'location_dest_id': dest_loc_id,
        })
        return picking
