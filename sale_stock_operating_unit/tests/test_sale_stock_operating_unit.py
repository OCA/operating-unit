# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common


class TestSaleStockOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestSaleStockOperatingUnit, self).setUp()
        self.res_groups = self.env['res.groups']
        self.res_users_model = self.env['res.users']
        self.warehouse_model = self.env['stock.warehouse']
        self.sale_model = self.env['sale.order']
        self.sale_line_model = self.env['sale.order.line']
        self.sale_team_model = self.env['crm.team']
        # Company
        self.company = self.env.ref('base.main_company')
        # Groups
        self.grp_sale_user = self.env.ref('sales_team.group_sale_manager')
        self.grp_acc_user = self.env.ref('account.group_account_invoice')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Customer
        self.customer = self.env.ref('base.res_partner_2')
        # Price list
        self.pricelist = self.env.ref('product.list0')
        # Products
        self.product1 = self.env.ref(
            'product.product_product_7')
        self.product1.write({'invoice_policy': 'order'})
        # Create user1
        self.user1 = self._create_user('user_1', [self.grp_sale_user,
                                                  self.grp_acc_user],
                                       self.company, [self.ou1, self.b2c])
        # Create user2
        self.user2 = self._create_user('user_2', [self.grp_sale_user,
                                                  self.grp_acc_user],
                                       self.company, [self.b2c])

        # Create sales team OU1
        self.sale_team_ou1 = self._create_sale_team(self.user1.id, self.ou1)

        # Create sales team OU2
        self.sale_team_b2c = self._create_sale_team(self.user2.id, self.b2c)

        # Warehouses
        self.ou1_wh = self.env.ref('stock.warehouse0')
        self.b2c_wh = self.env.ref('stock_operating_unit.stock_warehouse_b2c')
        # Locations
        self.b2c_wh.lot_stock_id.write({'company_id': self.company.id,
                                        'operating_unit_id': self.b2c.id})

        # Create Sale Order1
        self.sale1 = self._create_sale_order(self.user1.id, self.customer,
                                             self.product1, self.pricelist,
                                             self.sale_team_ou1, self.ou1_wh)
        # Create Sale Order2
        self.sale2 = self._create_sale_order(self.user2.id, self.customer,
                                             self.product1, self.pricelist,
                                             self.sale_team_b2c, self.b2c_wh)

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': 'Test Sales User',
            'login': login,
            'password': 'demo',
            'email': 'example@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_sale_team(self, uid, operating_unit):
        """Create a sale team."""
        team = self.sale_team_model.sudo(uid).with_context(
            mail_create_nosubscribe=True).create({
                'name': operating_unit.name,
                'operating_unit_id': operating_unit.id
            })
        return team

    def _create_sale_order(self, uid, customer, product, pricelist, team, wh):
        """Create a sale order."""
        sale = self.sale_model.sudo(uid).create({
            'partner_id': customer.id,
            'partner_invoice_id': customer.id,
            'partner_shipping_id': customer.id,
            'pricelist_id': pricelist.id,
            'team_id': team.id,
            'operating_unit_id': team.operating_unit_id.id,
            'warehouse_id': wh.id
        })
        self.sale_line_model.sudo(uid).create({
            'order_id': sale.id,
            'product_id': product.id,
            'name': 'Sale Order Line'
        })
        return sale

    def _confirm_sale(self, sale):
        sale.action_confirm()
        return True

    def test_security(self):
        """Test Sale Operating Unit"""
        # Confirm Sale1
        self._confirm_sale(self.sale1)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(self.sale1.operating_unit_id,
                         self.sale1.picking_ids.operating_unit_id,
                         'OU in Sale Order and Picking should be same')
        # Confirm Sale2
        self._confirm_sale(self.sale2)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(self.sale2.operating_unit_id,
                         self.sale2.picking_ids.operating_unit_id,
                         'OU in Sale Order and Picking should be same')
