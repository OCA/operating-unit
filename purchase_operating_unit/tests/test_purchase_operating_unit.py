# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tests import common


class TestPurchaseOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOperatingUnit, self).setUp()
        self.ResUsers = self.env['res.users']
        self.StockPicking = self.env['stock.picking']
        self.PurchaseOrder = self.env['purchase.order']
        self.AccountInvoice = self.env['account.invoice']
        # company
        self.company1 = self.env.ref('base.main_company')
        self.company2 = self.env.ref('stock.res_company_1')
        # groups
        self.group_purchase_user = self.env.ref('purchase.group_purchase_user')
        self.group_stock_user = self.env.ref('stock.group_stock_user')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2B Operating Unit
        self.b2b = self.env.ref('operating_unit.b2b_operating_unit')
        # Partner
        self.partner1 = self.env.ref('base.res_partner_1')
        # Products
        self.product1 = self.env.ref('product.product_product_7')
        self.product2 = self.env.ref('product.product_product_9')
        self.product3 = self.env.ref('product.product_product_11')
        # Account
        self.account = self.env.ref('l10n_generic_coa.conf_a_pay')
        # Create users
        self.user1_id = self._create_user('user_1',
                                          [self.group_purchase_user,
                                           self.group_stock_user],
                                          self.company1,
                                          [self.ou1])
        self.user2_id = self._create_user('user_2',
                                          [self.group_purchase_user,
                                           self.group_stock_user],
                                          self.company2,
                                          [self.b2b])
        self.purchase1 = self._create_purchase(
            self.user1_id, [(self.product1, 1000),
                            (self.product2, 500),
                            (self.product3, 800)])
        self.purchase1.sudo(self.user1_id).button_confirm()
        self._create_invoice(self.purchase1, self.partner1, self.account)

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

    def _create_purchase(self, user_id, line_products):
        """ Create a purchase order.
        ``line_products`` is a list of tuple [(product, qty)]
        """
        lines = []
        for product, qty in line_products:
            line_values = {
                'name': product.name,
                'product_id': product.id,
                'product_qty': qty,
                'product_uom': product.uom_id.id,
                'price_unit': 50,
                'date_planned': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            }
            lines.append((0, 0, line_values))
        purchase = self.PurchaseOrder.sudo(user_id).create({
            'operating_unit_id': self.ou1.id,
            'requesting_operating_unit_id': self.ou1.id,
            'partner_id': self.partner1.id,
            'order_line': lines,
            'company_id': self.company1.id,
        })
        return purchase

    def _create_invoice(self, purchase, partner, account):
        """ Create a vendor invoice for the purchase order."""
        invoice_vals = {
            'purchase_id': purchase.id,
            'partner_id': partner.id,
            'account_id': account.id,
            'type': 'in_invoice',
        }
        purchase_context = {
            'active_id': purchase.id,
            'active_ids': purchase.ids,
            'active_model': 'purchase.order',
        }
        self.env['account.invoice'].with_context(purchase_context).\
            create(invoice_vals)
        return True
