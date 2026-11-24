# Copyright 2026 Jarsa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Domain
from odoo.tests import tagged

from odoo.addons.hr_timesheet.tests.test_timesheet import TestCommonTimesheet


@tagged("post_install", "-at_install")
class TestTimesheetOperatingUnit(TestCommonTimesheet):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        cls.b2b = cls.env["operating.unit"].create(
            {
                "name": "B2B",
                "code": "B2B",
                "partner_id": cls.env.company.partner_id.id,
            }
        )
        cls.timesheets = cls.env["account.analytic.line"]
        for operating_unit, hours in ((cls.ou1, 2.0), (cls.b2b, 3.0), (cls.b2b, 1.0)):
            cls.timesheets |= cls.env["account.analytic.line"].create(
                {
                    "name": "Timesheet",
                    "project_id": cls.project_customer.id,
                    "task_id": cls.task1.id,
                    "employee_id": cls.empl_employee.id,
                    "unit_amount": hours,
                    "operating_unit_id": operating_unit.id,
                }
            )
        cls.env.flush_all()

    def test_report_operating_unit(self):
        report = self.env["timesheets.analysis.report"].search(
            Domain("id", "in", self.timesheets.ids)
        )
        self.assertEqual(len(report), 3)
        for line in report:
            timesheet = self.timesheets.browse(line.id)
            self.assertEqual(line.operating_unit_id, timesheet.operating_unit_id)

    def test_report_group_by_operating_unit(self):
        groups = self.env["timesheets.analysis.report"]._read_group(
            Domain("id", "in", self.timesheets.ids),
            ["operating_unit_id"],
            ["unit_amount:sum"],
        )
        self.assertEqual(dict(groups), {self.ou1: 2.0, self.b2b: 4.0})
