import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-analytic_operating_unit>=16.0dev,<16.1dev',
        'odoo-addon-operating_unit>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
