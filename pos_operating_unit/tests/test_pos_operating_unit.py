from odoo.exceptions import AccessError
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@tagged("post_install", "-at_install")
class TestPOSOperatingUnit(TestPoSCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = cls.basic_config
        # TestPoSCommon runs as the admin user, not as superuser
        cls.env.user.group_ids |= cls.env.ref(
            "operating_unit.group_manager_operating_unit"
        ) | cls.env.ref("operating_unit.group_multi_operating_unit")
        cls.product = cls.create_product("Product OU", cls.categ_basic, 10.0)

        OperatingUnit = cls.env["operating.unit"]
        cls.ou1 = OperatingUnit.create(
            {
                "name": "Main OU",
                "code": "MAIN",
                "company_id": cls.company.id,
                "partner_id": cls.company.partner_id.id,
            }
        )
        cls.b2b = OperatingUnit.create(
            {
                "name": "B2B OU",
                "code": "B2B",
                "company_id": cls.company.id,
                "partner_id": cls.company.partner_id.id,
            }
        )
        cls.config.operating_unit_ids = [Command.set(cls.ou1.ids)]

        groups = [
            Command.link(cls.env.ref("base.group_user").id),
            Command.link(cls.env.ref("point_of_sale.group_pos_manager").id),
            Command.link(cls.env.ref("account.group_account_invoice").id),
            Command.link(cls.env.ref("operating_unit.group_multi_operating_unit").id),
        ]
        # user1 belongs to the OU of the POS config, user2 does not
        cls.user1 = cls.env["res.users"].create(
            {
                "name": "User 1",
                "login": "pos_ou_user_1",
                "company_id": cls.company.id,
                "company_ids": [Command.set(cls.company.ids)],
                "group_ids": groups,
                "operating_unit_ids": [Command.set([cls.ou1.id, cls.b2b.id])],
                "default_operating_unit_id": cls.ou1.id,
            }
        )
        cls.user2 = cls.env["res.users"].create(
            {
                "name": "User 2",
                "login": "pos_ou_user_2",
                "company_id": cls.company.id,
                "company_ids": [Command.set(cls.company.ids)],
                "group_ids": groups,
                "operating_unit_ids": [Command.set(cls.b2b.ids)],
                "default_operating_unit_id": cls.b2b.id,
            }
        )

    def setUp(self):
        super().setUp()
        self.open_new_session()

    def test_operating_unit_access_config(self):
        configs_user1 = self.env["pos.config"].with_user(self.user1).search([])
        self.assertIn(self.config, configs_user1)
        configs_user2 = self.env["pos.config"].with_user(self.user2).search([])
        self.assertNotIn(self.config, configs_user2)

    def test_operating_unit_access_session(self):
        self.assertEqual(self.pos_session.operating_unit_ids, self.ou1)
        self.pos_session.with_user(self.user1).read()
        with self.assertRaises(AccessError):
            self.pos_session.with_user(self.user2).read()

    def test_operating_unit_access_order_and_line_and_payment(self):
        orders = self._create_orders(
            [
                {
                    "pos_order_lines_ui_args": [(self.product, 1)],
                    "payments": [(self.cash_pm1, 10.0)],
                }
            ]
        )
        order = list(orders.values())[0]
        self.assertEqual(order.operating_unit_ids, self.ou1)
        self.assertEqual(order.lines.operating_unit_ids, self.ou1)
        self.assertEqual(order.payment_ids.operating_unit_ids, self.ou1)
        order.with_user(self.user1).read()
        order.lines.with_user(self.user1).read()
        order.payment_ids.with_user(self.user1).read()
        with self.assertRaises(AccessError):
            order.with_user(self.user2).read()
        with self.assertRaises(AccessError):
            order.lines.with_user(self.user2).read()
        with self.assertRaises(AccessError):
            order.payment_ids.with_user(self.user2).read()
