##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

{
    "name": "Operating Unit in Products",
    "summary": "Adds the concept of operating unit (OU) in products",
    "version": "12.0.1.0.0",
    "author": "brain-tec AG, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Purchase Management",
    "depends": ["product", "stock"],
    "license": "LGPL-3",
    "data": [
        "security/product_template_security.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
}
