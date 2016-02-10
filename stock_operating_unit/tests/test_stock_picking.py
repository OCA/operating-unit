# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.addons.stock_operating_unit.tests import\
    test_stock_operating_unit as test_stock_ou


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
