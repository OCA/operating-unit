# Copyright 2016 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Requisitions",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow S.L.,"
    "Serpent Consulting Services Pvt. Ltd.,"
    "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Purchase Management",
    "depends": [
        "purchase_requisition_stock",
        "stock_operating_unit",
        "purchase_operating_unit",
    ],
    "data": [
        "view/purchase_requisition.xml",
        "security/purchase_security.xml",
    ],
    "installable": True,
}
