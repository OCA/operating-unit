# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.exceptions import ValidationError
from odoo.fields import Command, Domain

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestProductOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResUsers = cls.env["res.users"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.ProductCategory = cls.env["product.category"]
        cls.grp_user = cls.env.ref("base.group_user")
        # Products
        cls.product1 = cls.ProductTemplate.create(
            {
                "name": "Storage Box",
                "type": "consu",
                "standard_price": 14.0,
                "list_price": 15.8,
            }
        )
        cls.product2 = cls.ProductTemplate.create(
            {
                "name": "Pedal Bin",
                "type": "consu",
                "standard_price": 10.0,
                "list_price": 47.0,
            }
        )
        cls.product3 = cls.ProductTemplate.create(
            {
                "name": "Conference Chair",
                "type": "consu",
                "standard_price": 28.0,
                "list_price": 33.0,
            }
        )
        cls.product1.categ_id.operating_unit_ids = [Command.set([cls.ou1.id])]
        cls.product2.categ_id.operating_unit_ids = [Command.set([cls.b2b.id])]
        cls.product3.categ_id.operating_unit_ids = [
            Command.set([cls.ou1.id, cls.b2b.id])
        ]
        # Create User 1 with Main OU and B2B OU
        cls.user_ptest_1 = cls._create_user(
            "user_1_multi", cls.grp_ou_multi, cls.company, [cls.ou1, cls.b2b]
        )
        cls.user_ptest_1.group_ids = [Command.set([cls.grp_user.id])]
        # Create User 2 with B2B OU
        cls.user_ptest_2 = cls._create_user(
            "user_2_single", cls.grp_ou_mngr, cls.company, cls.b2b
        )
        cls.user_ptest_2.group_ids = [Command.set([cls.grp_user.id])]

    def test_po_ou_onchange(self):
        with self.assertRaises(ValidationError):
            self.product1.operating_unit_ids = [Command.set([self.b2b.id])]

    def test_po_ou_security(self):
        """Test Security of Product Operating Unit"""

        # User 1 is only assigned to Operating Unit 1, and can see all
        # products having Operating Unit 1.
        ou_domain = Domain("operating_unit_ids", "in", self.ou1.id)
        product_ids = (
            self.ProductTemplate.with_user(self.user_ptest_1).search(ou_domain).ids
        )
        category_ids = (
            self.ProductCategory.with_user(self.user_ptest_1).search(ou_domain).ids
        )
        self.assertIn(category_ids[0], product_ids)

        # User 2 is only assigned to Operating Unit 2, so cannot see products
        # having Operating Unit 1, expect those also having Operating Unit b2b
        product_ids = (
            self.ProductTemplate.with_user(self.user_ptest_2).search(ou_domain).ids
        )
        category_ids = (
            self.ProductCategory.with_user(self.user_ptest_2).search(ou_domain).ids
        )
        self.assertIn(category_ids[0], product_ids)

        # User 2 is only assigned to Operating Unit 2, and can see all
        # products having Operating Unit b2b.
        b2b_domain = Domain("operating_unit_ids", "in", self.b2b.id)
        product_ids = (
            self.ProductTemplate.with_user(self.user_ptest_2).search(b2b_domain).ids
        )
        category_ids = (
            self.ProductCategory.with_user(self.user_ptest_2).search(b2b_domain).ids
        )
        self.assertIn(category_ids[0], product_ids)

        # User 1 is only assigned to Operating Unit 1, so cannot see products
        # having Operating Unit b2b, expect those also having Operating Unit 1
        product_ids = (
            self.ProductTemplate.with_user(self.user_ptest_1).search(b2b_domain).ids
        )
        category_ids = (
            self.ProductCategory.with_user(self.user_ptest_2).search(b2b_domain).ids
        )
        self.assertIn(category_ids[0], product_ids)
