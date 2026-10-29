# Copyright 2026 Ametras Intelligence GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import itertools

from odoo.osv import expression
from odoo.tests import TransactionCase, new_test_user, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestStockMoveSecurity(TransactionCase):
    """A user sees the stock moves and move lines whose source and destination
    location have no operating unit or one of the user's operating units."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.env.company
        cls.unit_a, cls.unit_b = cls.env["operating.unit"].create(
            [
                {
                    "name": "Move Rule Unit %s" % code,
                    "code": "MRU%s" % code,
                    "partner_id": company.partner_id.id,
                    "company_id": company.id,
                }
                for code in ("A", "B")
            ]
        )
        Location = cls.env["stock.location"]
        locations = [
            Location.create(
                {
                    "name": "Move Rule %s" % unit.name,
                    "usage": "internal",
                    "operating_unit_id": unit.id,
                }
            )
            for unit in (cls.unit_a, cls.unit_b)
        ]
        locations.append(cls.env.ref("stock.stock_location_suppliers"))
        product = cls.env["product.product"].create(
            {"name": "Move Rule Product", "type": "product"}
        )
        cls.moves = cls.env["stock.move"]
        cls.move_lines = cls.env["stock.move.line"]
        for source, destination in itertools.product(locations, repeat=2):
            move = cls.env["stock.move"].create(
                {
                    "name": "%s -> %s" % (source.name, destination.name),
                    "product_id": product.id,
                    "product_uom": product.uom_id.id,
                    "product_uom_qty": 1.0,
                    "location_id": source.id,
                    "location_dest_id": destination.id,
                }
            )
            cls.moves |= move
            cls.move_lines |= cls.env["stock.move.line"].create(
                {
                    "move_id": move.id,
                    "product_id": product.id,
                    "product_uom_id": product.uom_id.id,
                    "location_id": source.id,
                    "location_dest_id": destination.id,
                }
            )
        cls.users = [
            new_test_user(
                cls.env,
                login="move_rule_user_%s" % index,
                groups="stock.group_stock_user",
                operating_unit_ids=[(6, 0, units.ids)],
                default_operating_unit_id=units[:1].id,
            )
            for index, units in enumerate(
                (cls.unit_a, cls.unit_a | cls.unit_b, cls.env["operating.unit"])
            )
        ]

    def _allowed(self, records, user):
        units = user.operating_unit_ids
        return records.filtered(
            lambda rec: (
                not rec.location_id.operating_unit_id
                or rec.location_id.operating_unit_id in units
            )
            and (
                not rec.location_dest_id.operating_unit_id
                or rec.location_dest_id.operating_unit_id in units
            )
        )

    def test_users_see_the_moves_of_their_operating_units(self):
        for user in self.users:
            for records in (self.moves, self.move_lines):
                with self.subTest(user=user.login, model=records._name):
                    visible = records.with_user(user).search(
                        [("id", "in", records.ids)]
                    )
                    expected = self._allowed(records, user)
                    self.assertEqual(
                        visible,
                        expected,
                        "%s should see the %s between locations without or with "
                        "one of its operating units: %s, not %s"
                        % (
                            user.login,
                            records._name,
                            expected.mapped("display_name"),
                            visible.sudo().mapped("display_name"),
                        ),
                    )

    def test_each_location_is_looked_up_once(self):
        """The rule on move lines reads each location field with one subquery.

        stock.move joins its locations (auto_join), so only move lines build
        subqueries; the SQL is built from this rule alone.
        """
        rule = self.env.ref(
            "stock_operating_unit.ir_rule_stock_move_line_allowed_operating_units"
        )
        domain = safe_eval(
            rule.domain_force, rule.with_user(self.users[0])._eval_context()
        )
        Line = self.env["stock.move.line"].sudo()
        sql, _params = expression.expression(domain, Line).query.select()
        self.assertEqual(
            sql.count('FROM "stock_location"'),
            2,
            "The operating unit rule on move lines should look up the source "
            "and the destination location once each:\n%s" % sql,
        )
