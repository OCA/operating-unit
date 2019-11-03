import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-account_operating_unit',
        'odoo11-addon-analytic_operating_unit',
        'odoo11-addon-crm_operating_unit',
        'odoo11-addon-hr_expense_operating_unit',
        'odoo11-addon-mis_builder_operating_unit',
        'odoo11-addon-operating_unit',
        'odoo11-addon-purchase_operating_unit',
        'odoo11-addon-sale_operating_unit',
        'odoo11-addon-sales_team_operating_unit',
        'odoo11-addon-stock_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
