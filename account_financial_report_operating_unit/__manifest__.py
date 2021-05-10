# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Financial Report OU",
    "version": "12.0.1.0.0",
    "category": "Reporting",
    "summary": "Operating Unit in OCA Financial Reports",
    "author": "ForgeFlow," "Odoo Community Association (OCA)",
    "website": "https://odoo-community.org/",
    "depends": ["account_financial_report", "account_operating_unit",],
    "data": [
        "wizard/open_items_wizard_view.xml",
        "wizard/aged_partner_balance_wizard_view.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
