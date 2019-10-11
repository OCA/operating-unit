##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo.addons.operating_unit.tests.OperatingUnitsTransactionCase import \
    OperatingUnitsTransactionCase


class TestResPartnerOperatingUnit(OperatingUnitsTransactionCase):

    def setUp(self):
        super(TestResPartnerOperatingUnit, self).setUp()

        self.ResUsers = self.env['res.users']
        self.ResPartner = self.env['res.partner']
        self.OperatingUnit = self.env['operating.unit']

        # Companies.
        self.company = self.env.ref('base.main_company')

        # Groups.
        self.group_partner_manager = self.env.ref('base.group_partner_manager')

        # Operating Units.
        self.opunit1 = self.OperatingUnit.create({
            'name': 'Operating Unit #1',
            'code': 'OP#1',
            'partner_id': self.env.ref('base.main_partner').id,
        })
        self.opunit2 = self.OperatingUnit.create({
            'name': 'Operating Unit #2',
            'code': 'OP#2',
            'partner_id': self.env.ref('base.main_partner').id,
        })

        # Partners.
        self.partner1 = self.env.ref('base.res_partner_1')
        self.partner2 = self.env.ref('base.res_partner_2')
        self.partner3 = self.env.ref('base.res_partner_3')
        self.partner_ids = [
            self.partner1.id, self.partner2.id, self.partner3.id]

        # Sets the operating-units for each partner.
        self.partner1.operating_unit_ids = [(6, False, [self.opunit1.id])]
        self.partner2.operating_unit_ids = [(6, False, [self.opunit2.id])]
        self.partner3.operating_unit_ids = [(6, False, [self.opunit1.id,
                                                        self.opunit2.id])]

        # Users.
        self.user1_id = self._create_user('user_1', self.group_partner_manager,
                                          self.company, self.opunit1).id
        self.user2_id = self._create_user('user_2', self.group_partner_manager,
                                          self.company, self.opunit2).id

    def test_operating_units_for_partners(self):
        """ Test Security of Partner Operating Unit
        """
        # User 1 is only assigned to Operating Unit 1, and can see all
        # contacts having Operating Unit 1.
        partners = self.ResPartner.sudo(self.user1_id).search([
            ('operating_unit_ids', 'in', self.opunit1.id),
            ('id', 'in', self.partner_ids),
        ])
        self.assertEqual(set(partners), {self.partner1, self.partner3})

        # User 2 is only assigned to Operating Unit 2, so cannot see contacts
        # having Operating Unit 1, except those also having Operating Unit 2.
        partners = self.ResPartner.sudo(self.user2_id).search([
            ('operating_unit_ids', 'in', self.opunit1.id),
            ('id', 'in', self.partner_ids),
        ])
        self.assertEqual(set(partners), {self.partner3})

        # User 2 is only assigned to Operating Unit 2, and can see all
        # contacts having Operating Unit Operating Unit 2.
        partners = self.ResPartner.sudo(self.user2_id).search([
            ('operating_unit_ids', 'in', self.opunit2.id),
            ('id', 'in', self.partner_ids),
        ])
        self.assertEqual(set(partners), {self.partner2, self.partner3})

        # User 1 is only assigned to Operating Unit 1, so cannot see contacts
        # having Operating Unit 2, except those also having Operating Unit 1.
        partners = self.ResPartner.sudo(self.user1_id).search([
            ('operating_unit_ids', 'in', self.opunit2.id),
            ('id', 'in', self.partner_ids),
        ])
        self.assertEqual(set(partners), {self.partner3})
