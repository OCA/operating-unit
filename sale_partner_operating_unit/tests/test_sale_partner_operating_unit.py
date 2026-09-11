# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.sale_operating_unit.tests.test_sale_operating_unit import (
    TestSaleOperatingUnit,
)


class TestSalePartnerOperatingUnit(TestSaleOperatingUnit):
    def test_sale_partner_operating_unit(self):
        # Check sale order is of the teams' OU
        self.assertEqual(
            self.sale1.operating_unit_id, self.sale_team_ou1.operating_unit_id
        )
        # Remove team from sale order
        self.sale1.write({"team_id": False})
        self.assertEqual(self.sale1.operating_unit_id, self.ou1)
        # Assign B2C OU to customer
        self.customer.write({"operating_unit_ids": [Command.set(self.b2c.ids)]})
        # Check sale order is of the customer's OU
        self.assertEqual(self.sale1.operating_unit_id, self.b2c)
        # Remove OU from customer
        self.customer.write({"operating_unit_ids": False})
        # Assign the team to the sale order
        self.sale1.write({"team_id": self.sale_team_b2c.id})
        # Check sale order is of the teams' OU
        self.assertEqual(
            self.sale1.operating_unit_id, self.sale_team_b2c.operating_unit_id
        )
