import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-operating-unit",
    description="Meta package for oca-operating-unit Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-account_operating_unit',
        'odoo9-addon-account_voucher_operating_unit',
        'odoo9-addon-analytic_operating_unit',
        'odoo9-addon-crm_claim_operating_unit',
        'odoo9-addon-crm_operating_unit',
        'odoo9-addon-hr_contract_operating_unit',
        'odoo9-addon-operating_unit',
        'odoo9-addon-procurement_operating_unit',
        'odoo9-addon-purchase_operating_unit',
        'odoo9-addon-purchase_request_operating_unit',
        'odoo9-addon-purchase_request_procurement_operating_unit',
        'odoo9-addon-purchase_request_qweb_operating_unit',
        'odoo9-addon-purchase_request_to_requisition_operating_unit',
        'odoo9-addon-purchase_request_to_rfq_operating_unit',
        'odoo9-addon-purchase_requisition_operating_unit',
        'odoo9-addon-report_qweb_operating_unit',
        'odoo9-addon-sale_operating_unit',
        'odoo9-addon-sale_stock_operating_unit',
        'odoo9-addon-sales_team_operating_unit',
        'odoo9-addon-stock_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
