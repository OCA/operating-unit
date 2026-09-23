# Copyright 2026 CIT Services - Solomon Prabu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import uuid
from datetime import timedelta

from odoo import fields
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestMisBuilderOU(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ou_model = cls.env["operating.unit"]
        cls.mis_report_model = cls.env["mis.report"]
        cls.mis_report_instance_model = cls.env["mis.report.instance"]
        cls.mis_report_instance_period_model = cls.env["mis.report.instance.period"]
        cls.company = cls.env.ref("base.main_company")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "company_id": cls.company.id,
                "is_company": True,
            }
        )
        unique_code1 = f"OU1_{uuid.uuid4().hex[:8]}"
        unique_code2 = f"OU2_{uuid.uuid4().hex[:8]}"
        # Create Operating Units
        cls.ou1 = cls.env["operating.unit"].create(
            {"name": unique_code1, "code": unique_code1, "partner_id": cls.partner.id}
        )
        cls.ou2 = cls.env["operating.unit"].create(
            {"name": unique_code2, "code": unique_code2, "partner_id": cls.partner.id}
        )
        # Create MIS Report
        cls.mis_report = cls.mis_report_model.create(
            {
                "name": "Test MIS Report",
            }
        )
        # Create MIS Report Instance
        cls.mis_instance = cls.mis_report_instance_model.create(
            {
                "name": "Test Instance",
                "report_id": cls.mis_report.id,
            }
        )
        # Create MIS period
        cls.mis_period = cls.mis_report_instance_period_model.create(
            {
                "name": "Test MIS Period",
                "report_instance_id": cls.mis_instance.id,
            }
        )

        partner_model_id = cls.env.ref("base.model_res_partner").id
        partner_create_date_field_id = cls.env.ref(
            "base.field_res_partner__create_date"
        ).id
        partner_debit_field_id = cls.env.ref("account.field_res_partner__debit").id

        # create a report
        cls.report = cls.mis_report_model.create(
            dict(
                name="test report",
                subkpi_ids=[
                    (0, 0, dict(name="sk1", description="subkpi 1", sequence=1)),
                    (0, 0, dict(name="sk2", description="subkpi 2", sequence=2)),
                ],
                query_ids=[
                    (
                        0,
                        0,
                        dict(
                            name="partner",
                            model_id=partner_model_id,
                            field_ids=[(4, partner_debit_field_id, None)],
                            date_field=partner_create_date_field_id,
                            aggregate="sum",
                        ),
                    )
                ],
            )
        )

    def test_operating_unit_ids_onchange_mis_instance(self):
        # Test has_no_operating_unit changes operating_unit_ids
        with Form(self.mis_instance) as form:
            form.comparison_mode = True
            form.has_no_operating_unit = True
        self.assertFalse(self.mis_instance.operating_unit_ids)

        with Form(self.mis_instance) as form:
            form.comparison_mode = True
            form.has_no_operating_unit = False
            form.operating_unit_ids.clear()
            form.operating_unit_ids.add(self.ou1)
        self.assertEqual(self.mis_instance.operating_unit_ids, self.ou1)

    def test_operating_unit_ids_onchange_mis_instance_period(self):
        # Test has_no_operating_unit changes operating_unit_ids
        with Form(self.mis_period) as form:
            form.manual_date_from = fields.Date.today() + timedelta(days=-14)
            form.manual_date_to = fields.Date.today() + timedelta(days=14)
            form.has_no_operating_unit = True
        self.assertFalse(self.mis_period.operating_unit_ids)

        with Form(self.mis_period) as form:
            form.manual_date_from = fields.Date.today() + timedelta(days=-14)
            form.manual_date_to = fields.Date.today() + timedelta(days=14)
            form.has_no_operating_unit = False
            form.operating_unit_ids.clear()
            form.operating_unit_ids.add(self.ou1)
        self.assertEqual(self.mis_period.operating_unit_ids, self.ou1)

    def test_get_additional_move_line_filter(self):
        period = self.env["mis.report.instance.period"].create(
            {
                "name": "Test Period",
                "report_instance_id": self.mis_instance.id,
            }
        )

        # Test filter with has_no_operating_unit=True
        self.mis_instance.write(
            {
                "has_no_operating_unit": True,
                "operating_unit_ids": [(6, 0, [self.ou1.id])],
            }
        )
        domain = period._get_additional_move_line_filter()
        self.assertIn("operating_unit_id", str(domain))
        self.assertIn("=", str(domain))
        self.assertIn("False", str(domain))

        # Test filter with no has_no_operating_unit but has operating_unit_ids
        self.mis_instance.write(
            {
                "has_no_operating_unit": False,
                "operating_unit_ids": [(6, 0, [self.ou1.id])],
            }
        )
        domain = period._get_additional_move_line_filter()
        self.assertIn("operating_unit_id", str(domain))
        self.assertIn("in", str(domain))
        self.assertIn(str(self.ou1.id), str(domain))

        # Test filter with no has_no_operating_unit and no operating_unit_ids
        self.mis_instance.write(
            {
                "has_no_operating_unit": False,
                "operating_unit_ids": [(5, 0, 0)],
            }
        )
        domain = period._get_additional_move_line_filter()
        self.assertNotIn("operating_unit_id", str(domain))

        # Test filter with has_no_operating_unit=True on the period
        period.write(
            {
                "has_no_operating_unit": True,
                "operating_unit_ids": [(6, 0, [self.ou1.id])],
            }
        )
        domain = period._get_additional_move_line_filter()
        self.assertIn("operating_unit_id", str(domain))
        self.assertIn("=", str(domain))
        self.assertIn("False", str(domain))

        # Test filter with operating_unit_ids on the period
        period.write(
            {
                "has_no_operating_unit": False,
                "operating_unit_ids": [(6, 0, [self.ou1.id])],
            }
        )
        domain = period._get_additional_move_line_filter()
        self.assertIn("operating_unit_id", str(domain))
        self.assertIn("in", str(domain))
        self.assertIn(str(self.ou1.id), str(domain))
