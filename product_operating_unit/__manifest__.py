# Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Unit in Products",
    "summary": "Adds the concept of operating unit (OU) in products",
    "version": "16.0.1.0.1",
    "author": "brain-tec AG, "
    "Open Source Integrators, "
    "Serpent Consulting Services Pvt. Ltd.,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Product",
    "depends": ["product", "operating_unit"],
    "license": "LGPL-3",
    "data": [
        "security/product_template_security.xml",
        "views/product_template_view.xml",
        "views/product_category_view.xml",
    ],
}
