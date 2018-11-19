# © 2017-TODAY Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.tests import common
from odoo.exceptions import AccessError


class TestOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users'].with_context(
            tracking_disable=True, no_reset_password=True)

        # Groups
        self.grp_ou_mngr = self.env.ref(
            'operating_unit.group_manager_operating_unit')
        self.grp_ou_multi = self.env.ref(
            'operating_unit.group_multi_operating_unit')
        # Company
        self.company = self.env.ref('base.main_company')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # B2B Operating Unit
        self.b2b = self.env.ref('operating_unit.b2b_operating_unit')
        # Create User 1 with Main OU
        self.user1 = self._create_user('user_1',
                                       self.grp_ou_mngr,
                                       self.company,
                                       self.ou1)
        # Create User 2 with B2C OU
        self.user2 = self._create_user('user_2',
                                       self.grp_ou_multi,
                                       self.company,
                                       self.b2c)

    def _create_user(self, login, group, company, operating_units,
                     context=None):
        """ Create a user. """
        user = self.res_users_model.create({
            'name': 'Test User',
            'login': login,
            'password': 'demo',
            'email': 'test@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'sel_groups_13_14': group.id
        })
        return user

    def _create_operating_unit(self, uid, name, code):
        """ Create Operating Unit"""
        ou = self.env['operating.unit'].sudo(uid).create({
            'name': name,
            'code': code,
            'partner_id': self.company.id,
        })
        return ou

    def test_01_operating_unit(self):
        # User 1 tries to create and modify an OU
        # Create
        self._create_operating_unit(self.user1.id, "Test", "TEST")
        # Write
        self.b2b.sudo(self.user1.id).write({'code': 'B2B_changed'})
        # Read list of OU available by User 1
        operating_unit_list_1 = self.env[
            'operating.unit'].sudo(self.user1.id).\
            search([]).mapped('code')
        self.assertEqual(len(operating_unit_list_1), 4,
                         'User 1 should have access to all the OU')

        # User 2 tries to create and modify an OU
        with self.assertRaises(AccessError):
            # Create
            self._create_operating_unit(self.user2.id, "Test", "TEST")
        with self.assertRaises(AccessError):
            # Write
            self.b2b.sudo(self.user2.id).write({'code': 'B2B_changed'})

        # Read list of OU available by User 2
        operating_unit_list_2 = self.env[
            'operating.unit'].sudo(self.user2.id).\
            search([]).mapped('code')
        self.assertEqual(len(operating_unit_list_2), 1,
                         'User 2 should have access to one OU')
        self.assertEqual(operating_unit_list_2[0], 'B2C',
                         'User 2 should have access to ' '%s' % self.b2c.name)
