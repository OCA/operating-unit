# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.payroll_operating_unit.tests.test_hr_payslip import TestPayslip


class TestPayslipAccess(TestPayslip):
    def setUp(self):
        super().setUp()

        # Groups
        self.grp_access_all = self.env.ref(
            "payroll_operating_unit_access_all.group_all_ou_payslip"
        )

        # Users
        self.user3 = self._create_user(
            "User_3",
            [self.grp_access_all, self.grp_payroll_mgr, self.group_user],
            self.env.company,
            [self.ou_second],
        )

    def test_ou_all_access(self):

        contracts = self.Contract.search([("employee_id", "=", self.richard_emp.id)])
        contracts.operating_unit_id = self.ou_main
        self.apply_contract_cron()
        richard_payslip = self.Payslip.create({"employee_id": self.richard_emp.id})
        richard_payslip.onchange_employee()

        self.assertEqual(
            richard_payslip.operating_unit_id, self.ou_main, "The payslip has OU main"
        )
        self.assertNotIn(
            self.ou_main,
            self.user3.operating_unit_ids,
            "OU main is NOT in user3's allowed OUs",
        )

        search_user3 = self.Payslip.with_user(self.user3).search(
            [
                ("employee_id", "=", self.richard_emp.id),
                ("operating_unit_id", "=", self.ou_main.id),
            ]
        )

        self.assertEqual(
            search_user3.ids,
            richard_payslip.ids,
            "User 3 has access to OU %s" % self.ou_main.name,
        )
