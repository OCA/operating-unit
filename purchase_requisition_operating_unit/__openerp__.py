# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Requisitions",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
    "Serpent Consulting Services Pvt. Ltd.,"
    "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Purchase Management",
    "depends": ["purchase_requisition", "purchase_operating_unit"],
    "data": [
        "view/purchase_requisition.xml",
        "security/purchase_security.xml",
    ],
    "installable": True,
}
