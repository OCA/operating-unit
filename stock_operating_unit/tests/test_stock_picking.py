# -*- coding: utf-8 -*-
# © 2016-2017 Eficent Business and IT Consulting Services S.L.
# © 2016-2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from . import test_stock_operating_unit as test_stock_ou


class TestStockPicking(test_stock_ou.TestStockOperatingUnit):

    def test_stock_picking_ou(self):
        """Test Pickings of Stock Operating Unit"""
        picking_ids = self.PickingObj.sudo(self.user1_id).\
            search([('id', '=', self.picking_in1.id)]).ids
        self.assertNotEqual(picking_ids, [], '')
        picking_ids = self.PickingObj.sudo(self.user2_id).\
            search([('id', '=', self.picking_in2.id)]).ids
        self.assertNotEqual(picking_ids, [])
        picking_ids = self.PickingObj.sudo(self.user1_id).\
            search([('id', '=', self.picking_int.id)]).ids
        self.assertNotEqual(picking_ids, [])
