import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-account_operating_unit',
        'odoo13-addon-analytic_operating_unit',
        'odoo13-addon-crm_operating_unit',
        'odoo13-addon-hr_contract_operating_unit',
        'odoo13-addon-hr_expense_operating_unit',
        'odoo13-addon-mrp_operating_unit',
        'odoo13-addon-operating_unit',
        'odoo13-addon-purchase_operating_unit',
        'odoo13-addon-report_qweb_operating_unit',
        'odoo13-addon-sale_operating_unit',
        'odoo13-addon-sales_team_operating_unit',
        'odoo13-addon-stock_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
