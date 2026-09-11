# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestProductPricelistOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_pricelist_model = cls.env["product.pricelist"]
        # Groups
        cls.grp_ou_system = cls.env.ref("base.group_system")
        # Create User 1 with Main OU
        cls.user_3 = cls._create_user(
            "user_3", cls.grp_ou_system, cls.company, [cls.ou1]
        )
        cls.user_3.write({"groups_id": [(4, cls.grp_ou_multi.id)]})
        # Create User 2 with B2C OU
        cls.user_4 = cls._create_user(
            "user_4", cls.grp_ou_system, cls.company, [cls.b2c]
        )
        cls.user_4.write({"groups_id": [(4, cls.grp_ou_multi.id)]})
        # Create Product Pricelists
        cls.pricelist1 = cls._create_product_pricelist(cls.user_3, cls.ou1)
        cls.pricelist2 = cls._create_product_pricelist(cls.user_4, cls.b2c)

    @classmethod
    def _create_product_pricelist(cls, user, operating_unit):
        """Create a Product Pricelist."""
        pricelist = cls.product_pricelist_model.with_user(user.id).create(
            {
                "name": "Product Pricelist",
                "operating_unit_id": operating_unit.id,
                "company_id": cls.company.id,
            }
        )
        return pricelist

    def test_00_security_product_pricelist(self):
        # User 4 is only assigned to Operating Unit B2C, and cannot
        # access Product Pricelist from Main Operating Unit.
        pricelist1 = self.product_pricelist_model.with_user(self.user_4.id).search(
            [("id", "=", self.pricelist1.id), ("operating_unit_id", "=", self.ou1.id)]
        )
        self.assertEqual(
            pricelist1.ids,
            [],
            "User 4 should not have access to " "%s" % self.ou1.name,
        )
        pricelist2 = self.product_pricelist_model.with_user(self.user_4.id).search(
            [("id", "=", self.pricelist2.id), ("operating_unit_id", "=", self.b2c.id)]
        )

        self.assertEqual(
            len(pricelist2.ids),
            1,
            f"User 4 should have access to OU {self.b2c.name}",
        )
