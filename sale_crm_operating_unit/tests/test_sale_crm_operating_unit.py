# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestSaleCrmOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestSaleCrmOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.crm_lead_model = self.env['crm.lead']
        self.sale_model = self.env['sale.order']
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Partner
        self.partner = self.env.ref('base.partner_root')

        # Create CRM Leads
        self.lead2 = self._create_crm_lead(self.ou1)

    def _create_crm_lead(self, operating_unit):
        """Create a sale order."""
        crm = self.crm_lead_model.create({
            'name': 'CRM LEAD',
            'partner_id': self.partner.id,
            'operating_unit_id': operating_unit.id,
            'type': 'opportunity'
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
