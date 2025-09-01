# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestPOSOperatingUnitBasic(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        # create partner and OU for the test to satisfy partner_id not-null
        partner = cls.env["res.partner"].create({"name": "OU Test Partner"})
        cls.ou = cls.env["operating.unit"].create(
            {
                "name": "OU Test",
                "code": "OUT",
                "company_id": cls.company.id,
                "partner_id": partner.id,
            }
        )

    def test_fields_and_assign(self):
        """Test POS configuration and session for operating units."""
        self.assertIn("operating_unit_ids", self.env["pos.config"]._fields)
        self.assertIn("operating_unit_ids", self.env["pos.session"]._fields)
        cfg = self.env["pos.config"].create(
            {
                "name": "POS Test",
                "company_id": self.company.id,
                "operating_unit_ids": [Command.set([self.ou.id])],
            }
        )
        self.assertIn(self.ou, cfg.operating_unit_ids)

    def test_operating_unit_assignment_via_write(self):
        """Ensure operating_unit_ids can be set via write and read back correctly."""
        cfg = self.env["pos.config"].create(
            {"name": "POS Write Test", "company_id": self.company.id}
        )
        self.assertFalse(cfg.operating_unit_ids)
        cfg.write({"operating_unit_ids": [Command.set([self.ou.id])]})
        self.assertIn(self.ou, cfg.operating_unit_ids)

    def test_operating_unit_unset_via_write(self):
        """Ensure operating_unit_ids can be unset via write."""
        cfg = self.env["pos.config"].create(
            {
                "name": "POS Unset Test",
                "company_id": self.company.id,
                "operating_unit_ids": [Command.set([self.ou.id])],
            }
        )
        self.assertIn(self.ou, cfg.operating_unit_ids)
        cfg.write({"operating_unit_ids": [Command.set([])]})
        self.assertFalse(cfg.operating_unit_ids)

    def test_assign_multiple_operating_units(self):
        """Assign multiple operating units to a config and verify both are present."""
        partner2 = self.env["res.partner"].create({"name": "OU2 Partner"})
        ou2 = self.env["operating.unit"].create(
            {
                "name": "OU 2",
                "code": "OU2",
                "company_id": self.company.id,
                "partner_id": partner2.id,
            }
        )
        cfg = self.env["pos.config"].create(
            {
                "name": "POS Multi OU",
                "company_id": self.company.id,
                "operating_unit_ids": [Command.set([self.ou.id, ou2.id])],
            }
        )
        self.assertIn(self.ou, cfg.operating_unit_ids)
        self.assertIn(ou2, cfg.operating_unit_ids)
        self.assertEqual(len(cfg.operating_unit_ids), 2)
