# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# © 2015 Serpent Consulting Services Pvt. Ltd..
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tests import common


class TestCrmClaimOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.crm_claim_model = self.env['crm.claim']
        self.crm_team_model = self.env['crm.team']

        self.company = self.env.ref('base.main_company')
        self.partner = self.env.ref('base.res_partner_1')
        self.grp_sale_manager = self.env.ref('base.group_sale_manager')

        # Main Operating Unit
        self.main_OU = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c_OU = self.env.ref('operating_unit.b2c_operating_unit')

        # Users
        self.user1 = self._create_user('user_1',
                                       [self.grp_sale_manager],
                                       self.company,
                                       [self.main_OU, self.b2c_OU])
        self.user2 = self._create_user('user_2',
                                       [self.grp_sale_manager],
                                       self.company,
                                       [self.b2c_OU])
        self.user3 = self._create_user('user_3',
                                       [self.grp_sale_manager],
                                       self.company,
                                       [self.main_OU, self.b2c_OU])
        # Teams
        self.team1 = self._create_crm_team(self.user1.id, self.main_OU)
        self.team2 = self._create_crm_team(self.user2.id, self.b2c_OU)

        # Claims
        self.crm_claim1 = self._create_crm_claim(self.user1.id, self.main_OU)
        self.crm_claim2 = self._create_crm_claim(self.user2.id, self.b2c_OU)
        self.crm_claim3 = self._create_crm_claim(self.user3.id)

    def _create_user(self, login, groups, company, operating_units):
        """Creates a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': login,
            'login': login,
            'password': 'demo',
            'email': 'example@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_crm_team(self, uid, operating_unit):
        """Create a CRM team."""
        context = {'mail_create_nosubscribe': True}
        crm = self.crm_team_model.create({
            'name': 'CRM team (' + operating_unit.name + ')',
            'operating_unit_id': operating_unit.id
        }, context=context)
        return crm

    def _create_crm_claim(self, uid, operating_unit=False):
        """Creates a CRM Claim."""
        if not operating_unit:
            operating_unit = self.crm_claim_model.sudo(uid).\
                _default_operating_unit()
        claim = self.crm_claim_model.sudo(uid).create({
            'name': " Damaged Products ",
            'operating_unit_id': operating_unit.id,
            'partner_id': self.partner.id,
            'user_id': uid,
            'team_id': self.crm_team_model.search(
                [('operating_unit_id', 'in', [operating_unit.id])],
                limit=1).id
            })
        claim.onchange_team_id()
        claim.onchange_operating_unit_id()
        return claim

    def test_security(self):
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # access claims of Main Operating Unit.
        record = self.crm_claim_model.sudo(
            self.user2.id).search([('id', '=', self.crm_claim1.id),
                                   ('operating_unit_id', '=',
                                    self.main_OU.id)])
        self.assertEqual(record.ids, [], 'User 2 should not have access to '
                         'OU %s.' % self.main_OU.name)

    def test_onchange(self):

        self.crm_claim3.operating_unit_id = self.b2c_OU
        self.crm_claim3.onchange_operating_unit_id()

        self.assertEqual(self.crm_claim3.team_id.operating_unit_id,
                         self.b2c_OU, 'User 3 should have '
                         'assigned the operating unit %s.' % self.b2c_OU)
