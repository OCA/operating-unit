# Copyright 2016-19 ForgeFlow S.L.
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, tools
from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestHrExpenseOperatingUnit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.res_users_model = cls.env["res.users"]
        cls.hr_expense_model = cls.env["hr.expense"]
        cls.hr_expense_sheet_model = cls.env["hr.expense.sheet"]
        cls.hr_employee_model = cls.env["hr.employee"]

        cls.company = cls.env.ref("base.main_company")
        cls.partner1 = cls.env.ref("base.res_partner_1")
        cls.partner2 = cls.env.ref("base.res_partner_2")

        # Expense Product
        cls.product1 = cls.env.ref("hr_expense.expense_product_mileage")

        cls.grp_hr_user = cls.env.ref("hr.group_hr_user")
        cls.grp_accou_mng = cls.env.ref("account.group_account_manager")
        cls.grp_account_invoice = cls.env.ref("account.group_account_invoice")

        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        cls.b2c = cls.env.ref("operating_unit.b2c_operating_unit")

        cls.user1 = cls._create_user(
            "Test HR User 1",
            "user_1",
            "demo1",
            [cls.grp_hr_user, cls.grp_accou_mng, cls.grp_account_invoice],
            cls.company,
            [cls.ou1, cls.b2c],
        )
        cls.user2 = cls._create_user(
            "Test HR User 2",
            "user_2",
            "demo2",
            [cls.grp_hr_user, cls.grp_accou_mng, cls.grp_account_invoice],
            cls.company,
            [cls.b2c],
        )

        cls.emp = cls._create_hr_employee()

        cls.hr_expense1 = cls._create_hr_expense(cls.ou1, cls.emp)

        cls.hr_expense2 = cls._create_hr_expense(cls.b2c, cls.emp)

    @classmethod
    def _create_user(
        cls, name, login, pwd, groups, company, operating_units, context=None
    ):
        """Creates a user."""
        group_ids = [group.id for group in groups]
        user = cls.res_users_model.create(
            {
                "name": name,
                "login": login,
                "password": pwd,
                "email": "example@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    @classmethod
    def _create_hr_employee(cls):
        """Creates an Employee."""
        emp = cls.hr_employee_model.create(
            {"name": "Test Employee", "address_home_id": cls.partner1.id}
        )
        return emp

    @classmethod
    def _create_hr_expense(cls, operating_unit, emp):
        """Creates Expense for employee."""
        hr_expense = cls.hr_expense_model.create(
            {
                "name": "Traveling Expense",
                "product_id": cls.product1.id,
                "operating_unit_id": operating_unit.id,
                "unit_amount": "10.0",
                "quantity": "5",
                "employee_id": emp.id,
            }
        )
        return hr_expense

    def _post_journal_entries(self, expense_sheet):
        """Approves the Expense and creates accounting entries."""
        expense_sheet.approve_expense_sheets()
        expense_sheet.action_sheet_move_create()
        self.assertEqual(
            expense_sheet.account_move_id.line_ids[0].operating_unit_id,
            expense_sheet.operating_unit_id,
        )

    def _register_payment(self, move_id, amount, ctx=False):
        if not ctx:
            ctx = {
                "active_ids": [move_id.id],
                "active_id": move_id.id,
                "active_model": "account.move",
            }
        PaymentWizard = self.env["account.payment.register"]
        with Form(PaymentWizard.with_context(**ctx)) as f:
            f.payment_date = fields.Date.today()
            f.amount = amount
        payment_wizard = f.save()
        payment_wizard.action_create_payments()

    def test_security(self):
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Expenses of Main Operating Unit.
        record = self.hr_expense_model.with_user(self.user2.id).search(
            [("id", "=", self.hr_expense1.id), ("operating_unit_id", "=", self.ou1.id)]
        )
        self.assertEqual(
            record.ids, [], "User 2 should not have access to %s" % self.ou1.name
        )
        # Create the expense sheet
        hr_expense_dict1 = self.hr_expense1.action_submit_expenses()
        sheet_context = hr_expense_dict1.get("context")
        sheet_dict = {
            "name": sheet_context.get("default_name", ""),
            "employee_id": sheet_context.get("default_employee_id", False),
            "company_id": sheet_context.get("default_company_id", False),
            "state": sheet_context.get("default_state", ""),
            "expense_line_ids": sheet_context.get("default_expense_line_ids", []),
        }
        self.hr_expense_sheet1 = self.hr_expense_sheet_model.create(sheet_dict)
        self._post_journal_entries(self.hr_expense_sheet1)
        # Expense OU should have same OU of its accounting entries
        self.assertEqual(
            self.hr_expense_sheet1.expense_line_ids.operating_unit_id,
            self.hr_expense_sheet1.account_move_id.line_ids.mapped("operating_unit_id"),
            "Expense OU should match with accounting entries OU",
        )
        self._register_payment(self.hr_expense_sheet1.account_move_id, 50.0)

    @tools.mute_logger(
        "odoo.addons.hr_expense_operating_unit.tests.test_hr_expense_operating_unit"
    )
    def test_constrains_error(self):
        hr_expense_dict1 = self.hr_expense1.action_submit_expenses()
        sheet_context = hr_expense_dict1.get("context")
        sheet_dict = {
            "name": sheet_context.get("default_name", ""),
            "employee_id": sheet_context.get("default_employee_id", False),
            "company_id": sheet_context.get("default_company_id", False),
            "state": sheet_context.get("default_state", ""),
            "expense_line_ids": sheet_context.get("default_expense_line_ids", []),
        }
        self.hr_expense_sheet1 = self.hr_expense_sheet_model.create(sheet_dict)
        with self.assertRaises(ValidationError):
            self.hr_expense_sheet1.expense_line_ids.write(
                {"operating_unit_id": self.b2c.id}
            )

        hr_expense_dict2 = self.hr_expense2.action_submit_expenses()
        sheet_context = hr_expense_dict2.get("context")
        sheet_dict = {
            "name": sheet_context.get("default_name", ""),
            "employee_id": sheet_context.get("default_employee_id", False),
            "company_id": sheet_context.get("default_company_id", False),
            "state": sheet_context.get("default_state", ""),
            "expense_line_ids": sheet_context.get("default_expense_line_ids", []),
        }
        with self.assertRaises(ValidationError):
            self.hr_expense_sheet2 = self.hr_expense_sheet_model.create(sheet_dict)

        self.hr_expense3 = self.hr_expense_model.create(
            {
                "name": "Traveling Expense",
                "product_id": self.product1.id,
                "unit_amount": "10.0",
                "quantity": "5",
                "operating_unit_id": False,
                "employee_id": self.emp.id,
            }
        )

        with self.assertRaises(ValidationError):
            self.hr_expense3.action_submit_expenses()
