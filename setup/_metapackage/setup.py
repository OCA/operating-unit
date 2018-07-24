import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-account_invoice_merge_operating_unit',
        'odoo10-addon-account_invoice_qweb_operating_unit',
        'odoo10-addon-account_operating_unit',
        'odoo10-addon-account_voucher_operating_unit',
        'odoo10-addon-analytic_operating_unit',
        'odoo10-addon-crm_operating_unit',
        'odoo10-addon-hr_contract_operating_unit',
        'odoo10-addon-hr_expense_operating_unit',
        'odoo10-addon-hr_payroll_account_operating_unit',
        'odoo10-addon-mis_builder_operating_unit',
        'odoo10-addon-mrp_operating_unit',
        'odoo10-addon-operating_unit',
        'odoo10-addon-procurement_operating_unit',
        'odoo10-addon-purchase_operating_unit',
        'odoo10-addon-purchase_request_operating_unit',
        'odoo10-addon-purchase_request_procurement_operating_unit',
        'odoo10-addon-purchase_request_to_rfq_operating_unit',
        'odoo10-addon-report_qweb_operating_unit',
        'odoo10-addon-sale_crm_operating_unit',
        'odoo10-addon-sale_operating_unit',
        'odoo10-addon-sale_stock_operating_unit',
        'odoo10-addon-sales_team_operating_unit',
        'odoo10-addon-stock_account_operating_unit',
        'odoo10-addon-stock_operating_unit',
        'odoo10-addon-stock_picking_qweb_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
