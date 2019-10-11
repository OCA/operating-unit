##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo.addons.operating_unit.tests.OperatingUnitsTransactionCase import \
    OperatingUnitsTransactionCase


class TestResPartnerCategoryOperatingUnit(OperatingUnitsTransactionCase):

    def setUp(self):
        super(TestResPartnerCategoryOperatingUnit, self).setUp()

        self.ResUsers = self.env['res.users']
        self.ResPartnerCategory = self.env['res.partner.category']
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

        # Partner categories
        self.partner_categ1 = self._create_partner_category('Categ. #1')
        self.partner_categ2 = self._create_partner_category('Categ. #2')
        self.partner_categ3 = self._create_partner_category('Categ. #3')

        # Sets the operating-units for each partner category.
        self.partner_categ1.operating_unit_ids = [
            (6, False, [self.opunit1.id])]
        self.partner_categ2.operating_unit_ids = [
            (6, False, [self.opunit2.id])]
        self.partner_categ3.operating_unit_ids = [
            (6, False, [self.opunit1.id, self.opunit2.id])]

        # Users.
        self.user1_id = self._create_user('user_1', self.group_partner_manager,
                                          self.company, self.opunit1).id
        self.user2_id = self._create_user('user_2', self.group_partner_manager,
                                          self.company, self.opunit2).id

    def _create_partner_category(self, name):
        """ Create a partner category.
        """
        return self.ResPartnerCategory.create({
            'name': name,
            'active': True,
        })

    def test_operating_units_for_partner_categories(self):
        """ Test Security of Partner's Category Operating Unit
        """
        # User 1 is only assigned to Operating Unit 1, and can see all
        # contact's tags having Operating Unit 1.
        partner_categs = self.ResPartnerCategory.sudo(self.user1_id).search([
            ('operating_unit_ids', 'in', self.opunit1.id),
        ])
        self.assertEqual(set(partner_categs), {self.partner_categ1,
                                               self.partner_categ3})

        # User 2 is only assigned to Operating Unit 2, so cannot see
        # contact's tags having Operating Unit 1, except those also having
        # Operating Unit 2.
        partner_categs = self.ResPartnerCategory.sudo(self.user2_id).search([
            ('operating_unit_ids', 'in', self.opunit1.id),
        ])
        self.assertEqual(set(partner_categs), {self.partner_categ3})

        # User 2 is only assigned to Operating Unit 2, and can see all
        # contact's tags having Operating Unit Operating Unit 2.
        partner_categs = self.ResPartnerCategory.sudo(self.user2_id).search([
            ('operating_unit_ids', 'in', self.opunit2.id),
        ])
        self.assertEqual(set(partner_categs), {self.partner_categ2,
                                               self.partner_categ3})

        # User 1 is only assigned to Operating Unit 1, so cannot see
        # contact's tags having Operating Unit 2, except those also having
        # Operating Unit 1.
        partner_categs = self.ResPartnerCategory.sudo(self.user1_id).search([
            ('operating_unit_ids', 'in', self.opunit2.id),
        ])
        self.assertEqual(set(partner_categs), {self.partner_categ3})
