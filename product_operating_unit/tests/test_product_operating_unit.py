##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo.tests import common


class TestProductOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestProductOperatingUnit, self).setUp()
        self.ResUsers = self.env['res.users']
        self.ProductTemplate = self.env['product.template']
        # company
        self.company1 = self.env.ref('base.main_company')
        self.company2 = self.env.ref('stock.res_company_1')
        # groups
        self.group_stock_user = self.env.ref('stock.group_stock_user')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2B Operating Unit
        self.b2b = self.env.ref('operating_unit.b2b_operating_unit')
        # Products
        self.product1 = self.env.ref(
            'product.product_product_1_product_template')
        self.product2 = self.env.ref(
            'product.product_product_9_product_template')
        self.product3 = self.env.ref(
            'product.product_product_11_product_template')
        # Create users
        self.user1_id = self._create_user('user_1',
                                          [self.group_stock_user],
                                          self.company1,
                                          [self.ou1])
        self.user2_id = self._create_user('user_2',
                                          [self.group_stock_user],
                                          self.company2,
                                          [self.b2b])
        self.product1.operating_unit_ids = [(6, 0, [self.ou1.id])]
        self.product2.operating_unit_ids = [(6, 0, [self.b2b.id])]
        self.product3.operating_unit_ids = [(6, 0, [self.ou1.id, self.b2b.id])]

    def _create_user(self, login, groups, company, operating_units):
        """ Create a user."""
        group_ids = [group.id for group in groups]
        user =\
            self.ResUsers.with_context({'no_reset_password': True}).\
            create({
                'name': 'Chicago Purchase User',
                'login': login,
                'password': 'demo',
                'email': 'chicago@yourcompany.com',
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'operating_unit_ids': [(4, ou.id) for ou in operating_units],
                'groups_id': [(6, 0, group_ids)]
            })
        return user.id

    def test_po_ou_security(self):
        """Test Security of Product Operating Unit"""

        # User 1 is only assigned to Operating Unit 1, and can see all
        # products having Operating Unit 1.
        product_ids = \
            self.ProductTemplate.sudo(self.user1_id).search(
                [('operating_unit_ids', 'in', self.ou1.id)]).ids
        self.assertEqual(set(product_ids), set([self.product1.id,
                                                self.product3.id]))

        # User 2 is only assigned to Operating Unit 2, so cannot see products
        # having Operating Unit 1, expect those also having Operating Unit b2b
        product_ids = \
            self.ProductTemplate.sudo(self.user2_id).search(
                [('operating_unit_ids', 'in', self.ou1.id)]).ids
        self.assertEqual(product_ids, [self.product3.id])

        # User 2 is only assigned to Operating Unit 2, and can see all
        # products having Operating Unit b2b.
        product_ids = \
            self.ProductTemplate.sudo(self.user2_id).search(
                [('operating_unit_ids', 'in', self.b2b.id)]).ids
        self.assertEqual(set(product_ids),
                         set([self.product2.id, self.product3.id]))

        # User 1 is only assigned to Operating Unit 1, so cannot see products
        # having Operating Unit b2b, expect those also having Operating Unit 1
        product_ids = \
            self.ProductTemplate.sudo(self.user1_id).search(
                [('operating_unit_ids', 'in', self.b2b.id)]).ids
        self.assertEqual(product_ids, [self.product3.id])
