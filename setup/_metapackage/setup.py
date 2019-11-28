import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-account_operating_unit',
        'odoo12-addon-analytic_operating_unit',
        'odoo12-addon-crm_operating_unit',
        'odoo12-addon-hr_contract_operating_unit',
        'odoo12-addon-hr_expense_operating_unit',
        'odoo12-addon-hr_payroll_account_operating_unit',
        'odoo12-addon-mrp_operating_unit',
        'odoo12-addon-operating_unit',
        'odoo12-addon-purchase_operating_unit',
        'odoo12-addon-purchase_request_operating_unit',
        'odoo12-addon-sale_operating_unit',
        'odoo12-addon-sales_team_operating_unit',
        'odoo12-addon-stock_account_operating_unit',
        'odoo12-addon-stock_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
