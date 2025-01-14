# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestSurveyOperatingUnit(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.ResUsers = self.env["res.users"]
        self.Survey = self.env["survey.survey"]
        self.UserInput = self.env["survey.user_input"]

        # Company
        self.company = self.env.ref("base.main_company")

        # Operating Units
        self.ou_main = self.env.ref("operating_unit.main_operating_unit")
        self.ou_secondary = self.env.ref("operating_unit.b2c_operating_unit")

        # Survey
        self.survey = self.Survey.create(
            {
                "title": "Customer Satisfaction Survey",
                "operating_unit_id": self.ou_main.id,
            }
        )

        # Users
        self.user_manager = self.ResUsers.create(
            {
                "name": "Manager",
                "login": "manager",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("survey.group_survey_user").id,
                        ],
                    )
                ],
                "operating_unit_ids": [(6, 0, [self.ou_main.id])],
            }
        )

    def test_survey_operating_unit_assignment(self):
        """Test that a survey is correctly assigned to the operating unit."""
        self.assertEqual(self.survey.operating_unit_id, self.ou_main)

    def test_user_input_operating_unit_restriction(self):
        """Test that user inputs are restricted by operating unit."""
        user_input = self.UserInput.create(
            {
                "survey_id": self.survey.id,
                "operating_unit_id": self.ou_main.id,
            }
        )
        self.assertEqual(user_input.operating_unit_id, self.ou_main)

        # Attempt to assign input to a different operating unit
        with self.assertRaises(ValidationError):
            user_input.operating_unit_id = self.ou_secondary.id

    def test_access_rights(self):
        """Test that only users with access to the operating unit can see related surveys."""
        self.survey.write({"operating_unit_id": self.ou_secondary.id})
        self.user_manager.operating_unit_ids = [(6, 0, [self.ou_main.id])]

        surveys = self.Survey.with_user(self.user_manager).search([])
        self.assertNotIn(self.survey, surveys)
