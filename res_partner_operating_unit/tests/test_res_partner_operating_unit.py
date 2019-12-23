# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common


class TestResPartnerOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestResPartnerOperatingUnit, self).setUp()
        self.res_partner_model = self.env['res.partner']
        self.res_users_model = self.env['res.users']
        # Company
        self.company = self.env.ref('base.main_company')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')

        # Create User 1 with Main OU
        self.user1 = self._create_user('user_1', self.company, [self.ou1])
        # Create User 2 with B2C OU
        self.user2 = self._create_user('user_2', self.company, [self.b2c])

        # Create Partner 1 with Main OU
        self.partner1 = self._create_partner('Test Partner 1', self.ou1)

        # Create Partner 2 with B2C OU
        self.partner2 = self._create_partner('Test Partner 2', self.b2c)

    def _create_partner(self, name, operating_unit, context=None):
        """ Create a partner. """
        partner = self.res_partner_model.create({
            'name': name,
            'operating_unit_id': operating_unit.id,
        })
        return partner

    def _create_user(self, login, company, operating_units,
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
        })
        return user
