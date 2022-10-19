import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-analytic_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-sales_team_operating_unit>=15.0dev,<15.1dev',
        'odoo-addon-stock_operating_unit>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
