import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_asset_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-account_financial_report_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-account_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-account_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-analytic_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-analytic_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-crm_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-hr_contract_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-hr_expense_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-hr_expense_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-hr_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-hr_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-hr_payroll_account_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-mis_builder_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-mis_builder_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-mrp_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-mrp_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-project_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-purchase_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-purchase_request_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-purchase_request_operating_unit_access_all>=15.0dev,<15.1dev',
        'odoo-addon-purchase_requisition_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-purchase_stock_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-report_qweb_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-sale_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-sale_stock_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-sales_team_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-stock_account_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-stock_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-stock_operating_unit_access_all>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
