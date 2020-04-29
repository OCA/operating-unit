from odoo import SUPERUSER_ID, api


def assign_ou_sequences(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        operating_unit_obj = env["operating.unit"]
        sequence_obj = env["ir.sequence"]
        for operating_unit in operating_unit_obj.search([]):
            purchase_sequence = sequence_obj.create(
                {
                    "name": "Purchase Order of {}".format(operating_unit.name),
                    "code": "purchase.order.{}".format(operating_unit.code),
                    "prefix": "{}-PO".format(operating_unit.code),
                    "padding": 5,
                    "company_id": operating_unit.company_id.id,
                }
            )
            operating_unit.write({"purchase_sequence_id": purchase_sequence.id})
