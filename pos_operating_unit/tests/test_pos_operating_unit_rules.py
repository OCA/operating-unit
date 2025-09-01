from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestPOSOperatingUnitRules(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.env.ref("base.main_company")
        # create partners for operating units to satisfy NOT NULL partner_id
        partner_a = cls.env["res.partner"].create({"name": "OU A Partner"})
        partner_b = cls.env["res.partner"].create({"name": "OU B Partner"})
        cls.ou_a = cls.env["operating.unit"].create(
            {
                "name": "OU A",
                "code": "OUA",
                "company_id": company.id,
                "partner_id": partner_a.id,
            }
        )
        cls.ou_b = cls.env["operating.unit"].create(
            {
                "name": "OU B",
                "code": "OUB",
                "company_id": company.id,
                "partner_id": partner_b.id,
            }
        )
        cls.user = cls.env["res.users"].create(
            {
                "name": "User A",
                "login": "user_a@example.com",
                "email": "user_a@example.com",
                "company_id": company.id,
                "operating_unit_ids": [(6, 0, [cls.ou_a.id])],
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            cls.env.ref("point_of_sale.group_pos_user").id,
                        ],
                    )
                ],
            }
        )
        # Sesión en OU_B (no autorizada para el user)
        cfg_b = cls.env["pos.config"].create(
            {
                "name": "POS B",
                "company_id": company.id,
                "operating_unit_ids": [Command.set([cls.ou_b.id])],
            }
        )
        cls.session_b = cls.env["pos.session"].create(
            {
                "config_id": cfg_b.id,
                "user_id": cls.env.ref("base.user_admin").id,
            }
        )

    def test_record_rule_hides_other_ou_sessions(self):
        """Test that the record rule hides POS sessions from other operating units."""
        sess = (
            self.env["pos.session"]
            .with_user(self.user)
            .search([("id", "=", self.session_b.id)])
        )
        self.assertFalse(sess, "User with OU_A must not see POS sessions from OU_B")
