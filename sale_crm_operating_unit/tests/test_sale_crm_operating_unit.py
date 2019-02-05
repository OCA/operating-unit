# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestSaleCrmOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestSaleCrmOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.crm_lead_model = self.env['crm.lead']
        self.sale_model = self.env['sale.order']
        self.grp_sale_mngr = self.env.ref('sales_team.group_sale_manager')
        self.grp_user = self.env.ref('base.group_user')
        self.crm_team_model = self.env['crm.team']
        # Company
        self.company = self.env.ref('base.main_company')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Partner
        self.partner = self.env.ref('base.partner_root')

        # Create CRM Leads
        self.lead2 = self._create_crm_lead(self.ou1)

        # Create User 1 with Main OU
        self.user1 = self._create_user('user_1', [self.grp_sale_mngr,
                                                  self.grp_user], self.company,
                                       [self.ou1])
        # Create User 2 with B2C OU
        self.user2 = self._create_user('user_2', [self.grp_sale_mngr,
                                                  self.grp_user], self.company,
                                       [self.b2c])
        # Create CRM teams
        self.team1 = self._create_crm_team(self.user1.id, self.ou1)

        self.team2 = self._create_crm_team(self.user2.id, self.b2c)

        # Create a CRM Lead with user 1 and team 1
        self.lead3 = self.crm_lead_model.create({
            'name': 'CRM2 LEAD',
            'partner_id': self.partner.id,
            'operating_unit': self.ou1.id,
            'type': 'opportunity',
            'user_id': self.user1.id,
            'team_id': self.team1.id
        })

    def _create_crm_lead(self, operating_unit):
        """Create a sale order."""
        crm = self.crm_lead_model.create({
            'name': 'CRM LEAD',
            'partner_id': self.partner.id,
            'operating_unit_id': operating_unit.id,
            'type': 'opportunity',
        })
        return crm

    def _create_user(self, login, groups, company, operating_units,
                     context=None):
        """ Create a user. """
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': 'Test User',
            'login': login,
            'password': 'demo',
            'email': 'test@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })

        return user

    def _create_crm_team(self, uid, operating_unit):
        """Create a Sales Team."""
        crm = self.crm_team_model.sudo(uid).create({'name': 'CRM team',
                                                    'operating_unit_id':
                                                        operating_unit.id,
                                                    })

        return crm

    def test_sale_crm(self):
        self.sale = self.sale_model.\
            with_context({'default_operating_unit_id':
                          self.lead2.operating_unit_id.id,
                          'default_opportunity_id': self.lead2.id}).\
            create({'partner_id': self.lead2.partner_id.id,
                    'team_id': self.lead2.team_id.id})
        # Assert that Operating Unit of Opportunity
        # matches to the Sale Order OU.
        self.assertEqual(self.sale.operating_unit_id,
                         self.sale.opportunity_id.operating_unit_id,
                         'Operating Unit of Opportunity should match to '
                         'the Sale Order Operating Unit.')

        # Checks that it raises the Warning if user tries to change
        # the Operating Unit
        with self.assertRaises(ValidationError):
            self.sale.operating_unit_id = self.b2c

    def test_salesperson(self):
        # Check that it raises the Warning if user tries to create a Sale Order
        # with a Salesperson who does not match with the Opportunities
        # Salesperson
        with self.assertRaises(ValidationError):
            self.sale_model.\
                with_context({'default_operating_unit_id':
                              self.lead3.operating_unit_id.id,
                              'default_opportunity_id': self.lead3.id}).\
                create({'partner_id': self.lead3.partner_id.id,
                        'user_id': self.user2.id,
                        'team_id': self.team1.id})

    def test_sales_team(self):
        # Check that it raises the Warning if user tries to create a Sale Order
        # with a Sales Channel that does not match with the Opportunities
        # Sales Channel
        with self.assertRaises(ValidationError):
            self.sale_model.\
                with_context({'default_operating_unit_id':
                              self.lead3.operating_unit_id.id,
                              'default_opportunity_id': self.lead3.id}).\
                create({'partner_id': self.lead3.partner_id.id,
                        'user_id': self.user1.id,
                        'team_id': self.team2.id})
