# Copyright 2026 Ametras Intelligence GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import new_test_user, tagged

from odoo.addons.stock_operating_unit.tests import test_stock_move_security


@tagged("post_install", "-at_install")
class TestStockMoveAccessAll(test_stock_move_security.TestStockMoveSecurity):
    """With this module the rules on stock moves and move lines keep their
    meaning for other users, and a user of the group sees all of them."""

    def test_group_sees_the_moves_of_all_operating_units(self):
        user = new_test_user(
            self.env,
            login="move_rule_user_all",
            groups="stock.group_stock_user,"
            "stock_operating_unit_access_all.group_all_ou_stock",
            operating_unit_ids=[(5, 0, 0)],
        )
        for records in (self.moves, self.move_lines):
            with self.subTest(model=records._name):
                self.assertEqual(
                    records.with_user(user).search([("id", "in", records.ids)]),
                    records,
                    "A user allowed to see the stock of all operating units "
                    "should see all %s" % records._name,
                )
