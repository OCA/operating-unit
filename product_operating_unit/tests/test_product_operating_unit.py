# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Command, Domain

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestProductOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductTemplate = cls.env["product.template"]
        cls.ProductCategory = cls.env["product.category"]
        cls.ou_a = cls.ou1
        cls.ou_b = cls.b2b
        cls.user_a = cls._create_user(
            "product_ou_a", cls.grp_ou_multi, cls.company, cls.ou_a
        )
        cls.user_b = cls._create_user(
            "product_ou_b", cls.grp_ou_multi, cls.company, cls.ou_b
        )
        cls.product_manager = cls._create_user(
            "product_ou_manager", cls.grp_ou_multi, cls.company, cls.ou_a
        )
        cls.product_manager.group_ids = [
            Command.link(cls.env.ref("product.group_product_manager").id)
        ]

        cls.category_a = cls._create_category("Category A", cls.ou_a)
        cls.category_b = cls._create_category("Category B", cls.ou_b)
        cls.category_ab = cls._create_category("Category A and B", cls.ou_a | cls.ou_b)
        cls.category_unassigned = cls._create_category(
            "Category without units", cls.env["operating.unit"]
        )
        cls.product_a = cls._create_product("Product A", cls.category_a)
        cls.product_b = cls._create_product("Product B", cls.category_b)
        cls.product_ab = cls._create_product("Product A and B", cls.category_ab)
        cls.product_unassigned = cls._create_product(
            "Product without units", cls.category_unassigned
        )

    @classmethod
    def _create_category(cls, name, units, **values):
        return cls.ProductCategory.create(
            {"name": name, "operating_unit_ids": [Command.set(units.ids)], **values}
        )

    @classmethod
    def _create_product(cls, name, category, **values):
        return cls.ProductTemplate.create(
            {"name": name, "categ_id": category.id, **values}
        )

    def _assert_visible(self, user, candidates, expected):
        visible = candidates.with_user(user).search(Domain("id", "in", candidates.ids))
        self.assertEqual(set(visible.ids), set(expected.ids))

    def _restrict_category_candidates(self, categories):
        # Isolate default selection from categories installed by other modules.
        self.env["ir.access"].create(
            {
                "name": "Read only the test categories",
                "model_id": self.env.ref("product.model_product_category").id,
                "operation": "r",
                "domain": repr([("id", "in", categories.ids)]),
            }
        )

    def test_01_product_inherits_category_units(self):
        self.assertEqual(self.product_a.operating_unit_ids, self.ou_a)

    def test_02_changing_category_recomputes_units(self):
        self.product_a.categ_id = self.category_b
        self.assertEqual(self.product_a.operating_unit_ids, self.ou_b)

    def test_03_category_units_propagate_to_product(self):
        self.category_a.operating_unit_ids = [Command.link(self.ou_b.id)]
        self.assertEqual(self.product_a.operating_unit_ids, self.ou_a | self.ou_b)

    def test_04_parent_category_units_propagate_to_descendants(self):
        child = self._create_category("Child", self.ou_a, parent_id=self.category_a.id)
        grandchild = self._create_category("Grandchild", self.ou_a, parent_id=child.id)
        descendant = self._create_product("Descendant product", grandchild)
        self.category_a.operating_unit_ids = [Command.link(self.ou_b.id)]
        self.assertEqual(descendant.operating_unit_ids, self.ou_a | self.ou_b)

    def test_05_propagation_preserves_additional_product_units(self):
        self.product_a.operating_unit_ids = [Command.link(self.b2c.id)]
        self.category_a.operating_unit_ids = [Command.link(self.ou_b.id)]
        self.assertEqual(
            self.product_a.operating_unit_ids, self.ou_a | self.ou_b | self.b2c
        )

    def test_06_product_units_must_include_category_units(self):
        with self.assertRaises(ValidationError):
            self.product_a.operating_unit_ids = [Command.set(self.ou_b.ids)]

    def test_07_exclusive_products_are_only_visible_to_assigned_users(self):
        products = self.product_a | self.product_b
        self._assert_visible(self.user_a, products, self.product_a)
        self._assert_visible(self.user_b, products, self.product_b)

    def test_08_product_with_both_units_is_visible_to_both_users(self):
        products = self.product_a | self.product_b | self.product_ab
        self._assert_visible(self.user_a, products, self.product_a | self.product_ab)
        self._assert_visible(self.user_b, products, self.product_b | self.product_ab)

    def test_09_product_without_units_is_visible_to_both_users(self):
        products = self.product_a | self.product_b | self.product_unassigned
        self._assert_visible(
            self.user_a, products, self.product_a | self.product_unassigned
        )
        self._assert_visible(
            self.user_b, products, self.product_b | self.product_unassigned
        )

    def test_10_category_visibility_follows_unit_assignments(self):
        categories = (
            self.category_a
            | self.category_b
            | self.category_ab
            | self.category_unassigned
        )
        self._assert_visible(
            self.user_a,
            categories,
            self.category_a | self.category_ab | self.category_unassigned,
        )
        self._assert_visible(
            self.user_b,
            categories,
            self.category_b | self.category_ab | self.category_unassigned,
        )

    def test_11_standard_company_restrictions_apply_without_units(self):
        other_category = self._create_category(
            "Other company category",
            self.env["operating.unit"],
            company_id=self.company_2.id,
        )
        other_product = self._create_product(
            "Other company product", other_category, company_id=self.company_2.id
        )
        other_user = self._create_user(
            "product_ou_other_company",
            self.grp_ou_multi,
            self.company_2,
            self.env["operating.unit"],
        )
        for user, expected_categories, expected_products in (
            (self.user_a, self.category_unassigned, self.product_unassigned),
            (
                other_user,
                self.category_unassigned | other_category,
                self.product_unassigned | other_product,
            ),
        ):
            self._assert_visible(
                user, self.category_unassigned | other_category, expected_categories
            )
            self._assert_visible(
                user, self.product_unassigned | other_product, expected_products
            )

    def test_12_creation_without_accessible_categories(self):
        self._restrict_category_candidates(self.category_b)
        categories = self.ProductCategory.with_user(self.product_manager)
        self.assertFalse(categories.search([]))
        products = self.ProductTemplate.with_user(self.product_manager)
        self.assertFalse(products.default_get(["categ_id"]).get("categ_id"))
        self.assertFalse(
            products.create({"name": "Without accessible category"}).categ_id
        )

    def test_13_default_category_matches_effective_product_company(self):
        company_category, other_category = self.ProductCategory.create(
            [
                {"name": "First company category", "company_id": self.company.id},
                {"name": "Second company category", "company_id": self.company_2.id},
            ]
        )
        self._restrict_category_candidates(company_category | other_category)
        self.product_manager.company_ids = [Command.link(self.company_2.id)]
        products = self.ProductTemplate.with_user(self.product_manager).with_context(
            allowed_company_ids=[self.company.id, self.company_2.id],
            default_company_id=self.company_2.id,
        )
        self.assertEqual(
            products.default_get(["categ_id", "company_id"])["categ_id"],
            other_category.id,
        )
        self.assertEqual(
            products.with_context(default_categ_id=False).default_get(["categ_id"]),
            {"categ_id": False},
        )
        first, second, shared = products.create(
            [
                {"name": "First company", "company_id": self.company.id},
                {"name": "Second company"},
                {"name": "Shared product", "company_id": False},
            ]
        )
        self.assertEqual(first.categ_id, company_category)
        self.assertEqual(second.categ_id, other_category)
        self.assertFalse(shared.categ_id)
        explicit = products.create(
            {
                "name": "Explicit category",
                "company_id": self.company.id,
                "categ_id": company_category.id,
            }
        )
        self.assertEqual(explicit.categ_id, company_category)

        variant = products.env["product.product"].create(
            {"name": "Direct variant", "company_id": self.company.id}
        )
        self.assertEqual(variant.categ_id, company_category)

    def test_14_granting_and_revoking_units_refreshes_visibility(self):
        products = self.product_a | self.product_b
        categories = self.category_a | self.category_b
        self._assert_visible(self.user_a, products, self.product_a)
        self._assert_visible(self.user_a, categories, self.category_a)
        self.user_a.assigned_operating_unit_ids = [Command.link(self.ou_b.id)]
        self._assert_visible(self.user_a, products, products)
        self._assert_visible(self.user_a, categories, categories)
        self.user_a.assigned_operating_unit_ids = [Command.unlink(self.ou_b.id)]
        self._assert_visible(self.user_a, products, self.product_a)
        self._assert_visible(self.user_a, categories, self.category_a)

    def test_15_direct_read_of_restricted_product_is_denied(self):
        visible = self.product_a.with_user(self.user_a)
        self.assertEqual(
            visible.read(["name"]), [{"id": visible.id, "name": "Product A"}]
        )
        with self.assertRaises(AccessError):
            self.product_b.with_user(self.user_a).read(["name"])

    def test_16_variants_inherit_template_visibility(self):
        variant_a = self.product_a.product_variant_id
        variant_b = self.product_b.product_variant_id
        variant_ab = self.product_ab.product_variant_id
        variant_unassigned = self.product_unassigned.product_variant_id
        variants = variant_a | variant_b | variant_ab | variant_unassigned
        self.assertEqual(len(variants), 4)
        self._assert_visible(
            self.user_a, variants, variant_a | variant_ab | variant_unassigned
        )
        self._assert_visible(
            self.user_b, variants, variant_b | variant_ab | variant_unassigned
        )
        self.assertFalse(
            self.env["ir.access"].search_count(
                [
                    ("model_id.model", "=", "product.product"),
                    ("domain", "ilike", "operating_unit_ids"),
                ]
            )
        )

    def test_17_rules_do_not_change_create_write_or_unlink_permissions(self):
        for model, visible, hidden, values in (
            (
                self.ProductTemplate,
                self.product_a,
                self.product_b,
                {"name": "New managed product", "categ_id": self.category_a.id},
            ),
            (
                self.ProductCategory,
                self.category_a,
                self.category_b,
                {"name": "New managed category"},
            ),
        ):
            with self.subTest(model=model._name):
                with self.assertRaises(AccessError):
                    model.with_user(self.user_a).create(values)
                with self.assertRaises(AccessError):
                    visible.with_user(self.user_a).write({"name": "Denied update"})
                with self.assertRaises(AccessError):
                    visible.with_user(self.user_a).unlink()
                hidden_as_manager = hidden.with_user(self.product_manager)
                self.assertFalse(hidden_as_manager.has_access("read"))
                self.assertTrue(hidden_as_manager.has_access("write"))
                self.assertTrue(hidden_as_manager.has_access("unlink"))
                record = model.with_user(self.product_manager).create(values)
                self.assertTrue(record.write({"name": "Managed update"}))
                self.assertTrue(record.unlink())

    def test_18_removing_units_from_category_keeps_product_units(self):
        self.category_ab.operating_unit_ids = [Command.unlink(self.ou_b.id)]
        self.assertEqual(self.category_ab.operating_unit_ids, self.ou_a)
        self.assertEqual(self.product_ab.operating_unit_ids, self.ou_a | self.ou_b)
