import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-analytic_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-contract_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-hr_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-product_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-project_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-report_qweb_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-sales_team_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-stock_operating_unit>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
