from odoo.exceptions import ValidationError

from odoo.addons.res_partner_operating_unit.tests.test_res_partner_operating_unit import (  # noqa: E501
    TestResPartnerOperatingUnit,
)


class TestPartnerPricelistOperatingUnit(TestResPartnerOperatingUnit):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Partners already created in `TestResPartnerOperatingUnit` class:
        # - cls.partner1:
        #   {"name": "Test Partner 1", "operating_unit_ids": [cls.ou1]}
        # - cls.partner2:
        #   {"name": "Test Partner 2", "operating_unit_ids": [cls.b2c]}
        cls.product_pricelist_model = cls.env["product.pricelist"]
        cls.pricelist1 = cls._create_product_pricelist(cls.ou1)
        cls.pricelist2 = cls._create_product_pricelist(cls.b2c)

        # Link Pricelists to Partners
        cls.partner1.property_product_pricelist = cls.pricelist1
        cls.partner2.property_product_pricelist = cls.pricelist2

    @classmethod
    def _create_product_pricelist(cls, operating_unit):
        """Create a Product Pricelist."""
        return cls.product_pricelist_model.create(
            {
                "name": "Product Pricelist",
                "operating_unit_id": operating_unit.id,
                "company_id": cls.company.id,
            }
        )

    def test_00_partner_pricelist_operating_unit(self):
        """Partners have correct pricelist within same OU"""
        self.assertEqual(self.partner1.property_product_pricelist, self.pricelist1)
        self.assertEqual(self.partner2.property_product_pricelist, self.pricelist2)

    def test_01_partner_pricelist_operating_unit(self):
        """Attempt to set a pricelist from another OU"""
        with self.assertRaises(ValidationError) as error:
            self.partner1.property_product_pricelist = self.pricelist2.id
        self.assertEqual(
            error.exception.args[0],
            "Pricelist 'Product Pricelist' belongs to "
            "Operating Unit 'B2C' "
            "which is not associated to this partner.",
        )
