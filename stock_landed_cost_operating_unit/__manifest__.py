{
    "name": "Stock Landed Costs with Operating Units",
    "summary": "Adds the concept of operating unit (OU) in Landed Costs",
    "version": "12.0.1.0.0",
    "category": "Stock",
    "author": "brain-tec AG,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["stock", "stock_landed_costs"],
    "data": [
        "security/stock_landed_cost_security.xml",
        "view/stock_landed_cost_views.xml",
    ],
    "installable": True,
    'uninstall_hook': 'uninstall_hook',
}
