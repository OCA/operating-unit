# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.hr_contract_operating_unit.tests\
    import test_hr_contract_operating_unit
from odoo.exceptions import UserError


class TestPayrollAccountOperatingUnit(test_hr_contract_operating_unit.
                                      TestHrContractOperatingUnit):

    def setUp(self):
        super(TestPayrollAccountOperatingUnit, self).setUp()
        self.hr_payslip_model = self.env['hr.payslip']
        self.acc_move_model = self.env['account.move']
        self.acc_journal_model = self.env['account.journal']

        self.hr_payroll_struct = self.env.ref('hr_payroll.structure_base')
        cash_account = self.env['account.account'].\
            search([('user_type_id', '=',
                     self.env.ref('account.data_account_type_liquidity').id)],
                   limit=1).id
        for line in self.hr_payroll_struct.rule_ids:
            line.account_debit = cash_account
            line.account_credit = cash_account
        # Add Payroll Salary Structure to Contract
        contracts = self.hr_contract1 + self.hr_contract2
        contracts.write({'struct_id': self.hr_payroll_struct.id})
        # Salary Journal
        self.journal = self.acc_journal_model.search([('type', '=', 'bank'),
                                                      ('name', '=', 'Bank')])
        # Create Payslip 1
        self.payslip1 = self._create_payslip(self.hr_contract1.id)
        # Create Payslip 2
        self.payslip2 = self._create_payslip(self.hr_contract2.id)

    def _create_payslip(self, contract):
        """Create a Pay-slip."""
        payslip = self.hr_payslip_model.create({
            'employee_id': self.emp.id,
            'contract_id': contract,
            'struct_id': self.hr_payroll_struct.id,
            'journal_id': self.journal.id
        })
        payslip.compute_sheet()
        payslip.action_payslip_done()
        return payslip

    def test_hr_payroll_account_ou(self):
        """Test Payroll Account Operating Unit"""
        with self.assertRaises(UserError):
            payslip = self.payslip1 + self.payslip2
            payslip.action_payslip_done()

        # Operating Unit (OU) of contract in Payslip should
        # match with OU of Accounting Entries of that Payslip
        self.assertEqual(self.payslip1.move_id.operating_unit_id,
                         self.payslip1.contract_id.operating_unit_id,
                         'Operating Unit (OU) of contract in Payslip should '
                         'match with Accounting Entries OU')
        self.assertEqual(self.payslip2.move_id.operating_unit_id,
                         self.payslip2.contract_id.operating_unit_id,
                         'Operating Unit (OU) of contract in Payslip should '
                         'match with Accounting Entries OU')
        self.assertEqual(self.payslip1.move_id.line_ids.
                         mapped('operating_unit_id'),
                         self.payslip1.contract_id.operating_unit_id,
                         'Operating Unit (OU) of contract in Payslip should '
                         'match with that of OU in Move lines')
        self.assertEqual(self.payslip2.move_id.line_ids.
                         mapped('operating_unit_id'),
                         self.payslip2.contract_id.operating_unit_id,
                         'Operating Unit (OU) of contract in Payslip should '
                         'match with that of OU in Move lines')
