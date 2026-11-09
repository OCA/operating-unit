# Copyright 2026 CIT-Services <https://cit-services.eu/>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.models import Command
from odoo.tests import tagged

from . import test_account_operating_unit as test_ou


@tagged("post_install", "-at_install")
class TestMulticompanyAccountOperatingUnit(test_ou.TestAccountOperatingUnit):
    def test_multi_company_default_ou_propagation(self):
        """
        The user's default operating unit is not propagated to an invoice
        when the default operating unit belongs to another company.
        """
        # same company
        self.user1.default_operating_unit_id = self.b2b
        result = (
            self.move_model.with_user(self.user1.id)
            .with_context(default_move_type="out_invoice")
            ._default_operating_unit_id()
        )
        self.assertEqual(result, self.b2b)

        # different company: user has access to company_2 but operates in company_1
        self.user1.company_ids = [Command.link(self.company_2.id)]
        self.user1.default_operating_unit_id = self.ou_company2
        result = (
            self.move_model.with_user(self.user1.id)
            .with_context(default_move_type="out_invoice")
            ._default_operating_unit_id()
        )
        self.assertFalse(
            result,
            "A default OU belonging to another company must not be applied "
            "to the invoice.",
        )
