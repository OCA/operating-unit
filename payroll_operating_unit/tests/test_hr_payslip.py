# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date

from odoo.addons.payroll.tests.common import TestPayslipBase


class TestPayslip(TestPayslipBase):
    def setUp(self):
        super().setUp()

        self.Contract = self.env["hr.contract"]
        self.OU = self.env["operating.unit"]
        self.Users = self.env["res.users"]

        # Operating Units
        self.default_ou = self.env.user.default_operating_unit_id
        self.ou_main = self.OU.create(
            {"name": "Main", "code": "M", "partner_id": self.env.company.id}
        )
        self.ou_second = self.OU.create(
            {"name": "Second", "code": "S", "partner_id": self.env.company.id}
        )

        # Groups
        self.grp_payroll_mgr = self.env.ref("payroll.group_payroll_manager")
        self.group_user = self.env.ref("base.group_user")

        # Users
        self.user1 = self._create_user(
            "User_1",
            [self.grp_payroll_mgr, self.group_user],
            self.env.company,
            [self.ou_main, self.ou_second],
        )
        self.user2 = self._create_user(
            "User_2",
            [self.grp_payroll_mgr, self.group_user],
            self.env.company,
            [self.ou_second],
        )

    def _create_user(self, login, groups, company, operating_units):
        return self.Users.create(
            {
                "name": f"Test Payslip {login}",
                "login": login,
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, [group.id for group in groups])],
            }
        )

    def test_ou_access(self):

        contracts = self.Contract.search([("employee_id", "=", self.richard_emp.id)])
        contracts.operating_unit_id = self.ou_main
        self.apply_contract_cron()
        richard_payslip = self.Payslip.create({"employee_id": self.richard_emp.id})
        richard_payslip.onchange_employee()

        self.assertEqual(
            richard_payslip.operating_unit_id, self.ou_main, "The payslip has OU main"
        )
        self.assertIn(
            self.ou_main,
            self.user1.operating_unit_ids,
            "OU main is in user1's allowed OUs",
        )

        search_user1 = self.Payslip.with_user(self.user1).search(
            [
                ("employee_id", "=", self.richard_emp.id),
                ("operating_unit_id", "=", self.ou_main.id),
            ]
        )
        search_user2 = self.Payslip.with_user(self.user2).search(
            [
                ("employee_id", "=", self.richard_emp.id),
                ("operating_unit_id", "=", self.ou_main.id),
            ]
        )

        self.assertEqual(
            search_user1.ids,
            richard_payslip.ids,
            "User 1 has access to OU %s" % self.ou_main.name,
        )
        self.assertEqual(
            search_user2.ids,
            [],
            "User 2 does NOT have access to OU %s" % self.ou_main.name,
        )

    def test_single_contract_default_ou(self):

        self.apply_contract_cron()
        richard_payslip = self.Payslip.create({"employee_id": self.richard_emp.id})

        self.assertEqual(
            self.richard_emp.default_operating_unit_id,
            self.default_ou,
            "There is default OU on EMPLOYEE",
        )
        contracts = self.Contract.search([("employee_id", "=", self.richard_emp.id)])
        self.assertEqual(
            contracts[0].operating_unit_id,
            self.default_ou,
            "There is default OU on CONTRACT",
        )
        self.assertEqual(
            richard_payslip.operating_unit_id,
            self.default_ou,
            "There is default OU on PAYSLIP",
        )

    def test_single_contract_oucontract(self):

        # Put OU on contract
        contracts = self.Contract.search([("employee_id", "=", self.richard_emp.id)])
        contracts.operating_unit_id = self.ou_main

        self.apply_contract_cron()
        richard_payslip = self.Payslip.create({"employee_id": self.richard_emp.id})
        richard_payslip.onchange_employee()

        self.assertEqual(
            richard_payslip.operating_unit_id,
            self.ou_main,
            "The OU on the payslip is same as CONTRACT",
        )

    def test_single_contract_ouemployee(self):

        # Put OU on employee
        self.richard_emp.default_operating_unit_id = self.ou_main

        contracts = self.Contract.search([("employee_id", "=", self.richard_emp.id)])
        self.apply_contract_cron()
        richard_payslip = self.Payslip.create({"employee_id": self.richard_emp.id})
        contracts.operating_unit_id = False
        richard_payslip.onchange_contract()

        self.assertFalse(contracts[0].operating_unit_id, "There is no OU on contract")
        self.assertEqual(
            richard_payslip.operating_unit_id,
            self.ou_main,
            "The OU on the payslip is same as EMPLOYEE",
        )

    def test_multi_contract(self):

        # Adjust richard's contracts to accomodate two of them
        contracts = self.Contract.search([("employee_id", "=", self.richard_emp.id)])
        today = date.today()
        contracts[0].date_start = date(today.year, today.month, 1)
        contracts[0].date_end = date(today.year, today.month, 14)
        c2 = self.Contract.create(
            {
                "date_end": False,
                "date_start": date(today.year, today.month, 15),
                "name": "Contract #2 for Richard",
                "wage": 5000.0,
                "employee_id": self.richard_emp.id,
                "struct_id": self.developer_pay_structure.id,
                "kanban_state": "done",
            }
        )

        # Set operating units
        contracts[0].operating_unit_id = self.ou_main
        c2.operating_unit_id = self.ou_second

        self.apply_contract_cron()
        richard_payslip = self.Payslip.create({"employee_id": self.richard_emp.id})
        richard_payslip.onchange_employee()

        self.assertEqual(
            richard_payslip.operating_unit_id,
            self.ou_main,
            "The OU on the payslip is same as 1st CONTRACT",
        )
