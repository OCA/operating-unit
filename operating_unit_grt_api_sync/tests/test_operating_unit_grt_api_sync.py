from datetime import datetime

from odoo.tests import common


class TestOperatingUnitGrtApiSync(common.TransactionCase):
    def setUp(self):
        super(TestOperatingUnitGrtApiSync, self).setUp()
        self.OperatingUnit = self.env["operating.unit"]
        date_today = datetime.today()
        date_tomorrow = date_today.replace(day=date_today.day + 1)
        date_yesterday = date_today.replace(day=date_today.day - 1)
        date_2_years_ago = date_today.replace(year=date_today.year - 2)
        date_3_years_ago = date_today.replace(year=date_today.year - 3)
        date_3_years_later = date_today.replace(year=date_today.year + 3)
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        self.ou2 = self.env.ref("operating_unit.b2b_operating_unit")
        self.ou3 = self.env.ref("operating_unit.b2c_operating_unit")
        self.ou_to_update_valid_from = date_yesterday
        self.ou_to_update_valid_until = date_3_years_later
        self.ou_to_update = self.env["operating.unit"].create(
            {
                "name": "Test OU",
                "code": "PDE1204",
                "partner_id": self.env["res.partner"]
                .create({"name": "Test Partner"})
                .id,
                "valid_from": date_yesterday,
                "valid_until": date_3_years_later,
            }
        )
        self.ou_not_present_in_api = self.env["operating.unit"].create(
            {
                "name": "Non-existing OU",
                "code": "UNKNOWN",
                "partner_id": self.env["res.partner"]
                .create({"name": "Unknown Partner"})
                .id,
                "valid_from": date_3_years_ago,
                "valid_until": False,
            }
        )

        # Not a branch MID
        self.mid_to_skip_data = {
            "management_id": "MID1",
            "simple_name": "Prüfservice",
            "management_id_level_number": 12,
            "management_id_level": "Business Unit",
            "is_leaf": False,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": None,
            "operational_until": None,
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "BUMID1",
            "l10_operating_country": None,
            "l10_operating_country_management_id": None,
            "l8_operating_unit": None,
            "l8_operating_unit_management_id": None,
            "l5_branch": None,
            "l5_branch_management_id": None,
        }

        # MID active in the past, to be created
        self.mid_to_create_1_data = {
            "management_id": "PDE1101",
            "simple_name": "Villingen-Schwenningen",
            "management_id_level_number": 5,
            "management_id_level": "Branch",
            "is_leaf": True,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": datetime.strftime(date_3_years_ago, "%Y-%m-%d"),
            "operational_until": datetime.strftime(date_2_years_ago, "%Y-%m-%d"),
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "MID1",
            "l10_operating_country": "Germany",
            "l10_operating_country_management_id": "PDE0000",
            "l8_operating_unit": "Freiburg",
            "l8_operating_unit_management_id": "PDE1100",
            "l5_branch": "Villingen-Schwenningen",
            "l5_branch_management_id": "PDE1101",
        }

        # MID active in the future, to be created
        self.mid_to_create_2_data = {
            "management_id": "PDE1102",
            "simple_name": "Villingen-Schwenningen",
            "management_id_level_number": 5,
            "management_id_level": "Branch",
            "is_leaf": True,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": datetime.strftime(date_3_years_later, "%Y-%m-%d"),
            "operational_until": None,
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "MID1",
            "l10_operating_country": "Germany",
            "l10_operating_country_management_id": "PDE0000",
            "l8_operating_unit": "Freiburg",
            "l8_operating_unit_management_id": "PDE1100",
            "l5_branch": "Villingen-Schwenningen",
            "l5_branch_management_id": "PDE1102",
        }

        # MID active today, to be created
        self.mid_to_create_3_data = {
            "management_id": "PDE1201",
            "simple_name": "Fulda",
            "management_id_level_number": 5,
            "management_id_level": "Branch",
            "is_leaf": True,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": datetime.strftime(date_3_years_ago, "%Y-%m-%d"),
            "operational_until": datetime.strftime(date_3_years_later, "%Y-%m-%d"),
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "MID1",
            "l10_operating_country": "Germany",
            "l10_operating_country_management_id": "PDE0000",
            "l8_operating_unit": "Fulda",
            "l8_operating_unit_management_id": "PDE1200",
            "l5_branch": "Fulda",
            "l5_branch_management_id": "PDE1201",
        }

        # MID active since today, to be created
        self.mid_to_create_4_data = {
            "management_id": "PDE1202",
            "simple_name": "Fulda",
            "management_id_level_number": 5,
            "management_id_level": "Branch",
            "is_leaf": True,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": datetime.strftime(date_today, "%Y-%m-%d"),
            "operational_until": None,
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "MID1",
            "l10_operating_country": "Germany",
            "l10_operating_country_management_id": "PDE0000",
            "l8_operating_unit": "Fulda",
            "l8_operating_unit_management_id": "PDE1200",
            "l5_branch": "Fulda",
            "l5_branch_management_id": "PDE1202",
        }

        # MID without operational dates, to be created
        self.mid_to_create_5_data = {
            "management_id": "PDE1203",
            "simple_name": "Fulda",
            "management_id_level_number": 5,
            "management_id_level": "Branch",
            "is_leaf": True,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": None,
            "operational_until": None,
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "MID1",
            "l10_operating_country": "Germany",
            "l10_operating_country_management_id": "PDE0000",
            "l8_operating_unit": "Fulda",
            "l8_operating_unit_management_id": "PDE1200",
            "l5_branch": "Fulda",
            "l5_branch_management_id": "PDE1203",
        }

        # MID with updated operational dates, to be updated
        self.mid_to_update_1_data = {
            "management_id": "PDE1204",
            "simple_name": "Fulda",
            "management_id_level_number": 5,
            "management_id_level": "Branch",
            "is_leaf": True,
            "is_office": False,
            "is_operational_today": True,
            "is_operational_in_reference_range": True,
            "operational_from": date_tomorrow.strftime("%Y-%m-%d"),
            "operational_until": date_3_years_later.strftime("%Y-%m-%d"),
            "l12_business_unit": "Prüfservice",
            "l12_business_unit_management_id": "MID1",
            "l10_operating_country": "Germany",
            "l10_operating_country_management_id": "PDE0000",
            "l8_operating_unit": "Fulda",
            "l8_operating_unit_management_id": "PDE1200",
            "l5_branch": "Fulda",
            "l5_branch_management_id": "PDE1204",
        }

        self.sample_response_data = [
            self.mid_to_skip_data,
            self.mid_to_create_1_data,
            self.mid_to_create_2_data,
            self.mid_to_create_3_data,
            self.mid_to_create_4_data,
            self.mid_to_create_5_data,
            self.mid_to_update_1_data,
        ]

    def test_01_create_operating_unit(self):
        """Test that the operating units data received from the API created MIDs."""
        api_data = self.sample_response_data
        self.env["operating.unit"]._process_grt_branch_data(api_data)

        ou_1 = self.OperatingUnit.search(
            [("code", "=", self.mid_to_create_1_data["l5_branch_management_id"])]
        )
        self.assertTrue(
            ou_1,
            f"MID with code {self.mid_to_create_1_data['l5_branch_management_id']} should have been created.",
        )
        ou_1_name = f"{self.mid_to_create_1_data['l5_branch_management_id']} - OU {self.mid_to_create_1_data['l8_operating_unit']}, Branch {self.mid_to_create_1_data['l5_branch']}"
        ou_1_partner_name = f"OU {self.mid_to_create_1_data['l8_operating_unit']}, Branch {self.mid_to_create_1_data['l5_branch']}"
        self.assertEqual(
            ou_1.name,
            ou_1_name,
            "Name of OU 1 should be of the following format: code - OU branch, OU Office",
        )
        ou_1_partner_created = self.env["res.partner"].search(
            [("name", "=", ou_1_partner_name)]
        )
        self.assertTrue(
            ou_1_partner_created,
            f"Partner with name {self.mid_to_create_1_data['simple_name']} should have been created.",
        )
        self.assertTrue(
            datetime.strftime(ou_1.valid_from, "%Y-%m-%d")
            == self.mid_to_create_1_data["operational_from"],
            "Valid from date should be the same as the one in the API response.",
        )
        self.assertTrue(
            datetime.strftime(ou_1.valid_until, "%Y-%m-%d")
            == self.mid_to_create_1_data["operational_until"],
            "Valid until date should be the same as the one in the API response.",
        )
        self.assertEqual(
            ou_1.validity_state,
            "expired",
            "OU1: Validity state should be set to 'expired'.",
        )
        self.assertEqual(
            ou_1.synced_with_grt, True, "OU1: Should be flagged as synced with the API."
        )

        ou_2 = self.OperatingUnit.search(
            [("code", "=", self.mid_to_create_2_data["l5_branch_management_id"])]
        )
        self.assertTrue(
            ou_2,
            f"MID with code {self.mid_to_create_2_data['l5_branch_management_id']} should have been created.",
        )
        self.assertEqual(
            ou_2.validity_state,
            "not_valid_yet",
            "OU2: Validity state should be set to 'not_valid_yet'.",
        )

        ou_3 = self.OperatingUnit.search(
            [("code", "=", self.mid_to_create_3_data["l5_branch_management_id"])]
        )
        self.assertTrue(
            ou_3,
            f"MID with code {self.mid_to_create_3_data['l5_branch_management_id']} should have been created.",
        )
        self.assertEqual(
            ou_3.validity_state,
            "valid",
            "OU3: Validity state should be set to 'valid'.",
        )

        ou_4 = self.OperatingUnit.search(
            [("code", "=", self.mid_to_create_4_data["l5_branch_management_id"])]
        )
        self.assertTrue(
            ou_4,
            f"MID with code {self.mid_to_create_4_data['l5_branch_management_id']} should have been created.",
        )
        self.assertEqual(
            ou_4.validity_state,
            "valid",
            "OU4: Validity state should be set to 'valid'.",
        )

        ou_5 = self.OperatingUnit.search(
            [("code", "=", self.mid_to_create_5_data["l5_branch_management_id"])]
        )
        self.assertTrue(
            ou_5,
            f"MID with code {self.mid_to_create_5_data['l5_branch_management_id']} should have been created.",
        )
        self.assertEqual(
            ou_5.validity_state,
            "valid",
            "OU5: Validity state should be set to 'valid'.",
        )

        ou_to_skip = self.OperatingUnit.search(
            [("code", "=", self.mid_to_skip_data["management_id"])]
        )
        self.assertFalse(
            ou_to_skip,
            f"MID with code {self.mid_to_skip_data['management_id']} should not have been created.",
        )

    def test_02_update_operating_unit(self):
        """Test that the operating units data received from the API updates existing MIDs."""
        self.env["operating.unit"]._process_grt_branch_data([self.mid_to_update_1_data])

        self.assertEqual(
            datetime.strftime(self.ou_to_update.valid_from, "%Y-%m-%d"),
            self.mid_to_update_1_data["operational_from"],
            "Valid from date should have been updated to the date received from the API.",
        )
        self.assertEqual(
            datetime.strftime(self.ou_to_update.valid_until, "%Y-%m-%d"),
            self.mid_to_update_1_data["operational_until"],
            "Valid until date should have been updated to the date received from the API.",
        )

    def test_03_mark_mid_as_not_synced_with_api(self):
        """Test that the MID is flagged as 'not synced with GRT API' if no related data for it is present in the API response."""
        self.env["operating.unit"]._process_grt_branch_data(self.sample_response_data)

        self.assertEqual(
            self.ou_not_present_in_api.synced_with_grt,
            False,
            "OU should be flagged as not synced with the API.",
        )
