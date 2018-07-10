# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestMrpOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestMrpOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.mrp_production_model = self.env['mrp.production']
        self.company = self.env.ref('base.main_company')
        self.bom_id = self.env.ref('mrp.mrp_bom_manufacture')

        # Products
        self.product1 = self.env.ref('product.product_product_4c')
        # Stock Location
        self.stock_location = self.env.ref('stock.stock_location_shop0')

        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # Chicago Operating Unit
        self.chicago = \
            self.env.ref('stock_operating_unit.operating_unit_shop0')
        # Groups
        self.grp_mrp_saleman = self.env.ref('sales_team.group_sale_salesman')
        self.grp_mrp_manager = self.env.ref('mrp.group_mrp_manager')

        # Users
        self.user1 = self._create_user(
            'user_1', [self.grp_mrp_saleman],
            self.company, [self.ou1, self.chicago])
        self.user2 = self._create_user(
            'user_2', [self.grp_mrp_saleman, self.grp_mrp_manager],
            self.company, [self.chicago])

        # Manufacturing Orders
        self.mrp_record1 = self._create_mrp('Manufacturing Order 1', self.ou1)
        self.mrp_record2 = self._create_mrp('Manufacturing Order 2',
                                            self.chicago, self.stock_location)

    def _create_user(self, login, groups, company, operating_units,
                     context=None):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': 'Test HR Contrac User',
            'login': login,
            'password': 'demo',
            'email': 'example@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_mrp(self, name, operating_unit, stock_location=False):
        if operating_unit == self.ou1:
            mrp = self.mrp_production_model.create({
                'name': name,
                'product_id': self.product1.id,
                'bom_id': self.bom_id.id,
                'product_qty': '10.0',
                'product_uom_id': self.product1.uom_id.id,
                'operating_unit_id': operating_unit.id,
            })
        else:
            mrp = self.mrp_production_model.create({
                'name': name,
                'product_id': self.product1.id,
                'bom_id': self.bom_id.id,
                'product_qty': '10.0',
                'product_uom_id': self.product1.uom_id.id,
                'operating_unit_id': operating_unit.id,
                'location_src_id': stock_location.id,
                'location_dest_id': stock_location.id
            })
        return mrp

    def test_mrp_ou(self):
        record = self.mrp_production_model.sudo(self.user2.id).\
            search([('id', '=', self.mrp_record1.id),
                    ('operating_unit_id', '=', self.ou1.id)])
        self.assertEqual(record.ids, [], 'User 2 should not have access to '
                         'OU : %s' % self.ou1.name)

        with self.assertRaises(ValidationError):
            self.mrp_record1.operating_unit_id = False
        with self.assertRaises(ValidationError):
            self.mrp_record1.write({'operating_unit_id': self.chicago.id})
