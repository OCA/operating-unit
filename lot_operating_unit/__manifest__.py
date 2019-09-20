##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

{
    "name": "Operating Unit in Lots",
    "summary": "Adds the concept of operating unit (OU) in lots",
    "version": "12.0.1.0.0",
    "author": "brain-tec AG, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Warehouse",
    "depends": [
        "stock",
        "operating_unit",
        "product_operating_unit",
    ],
    "license": "LGPL-3",
    "data": [
        "security/stock_production_lot_security.xml",
    ],
    "installable": True,
}
