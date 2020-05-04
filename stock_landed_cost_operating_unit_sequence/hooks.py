from odoo import SUPERUSER_ID, api


def assign_ou_sequences(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        operating_unit_obj = env["operating.unit"]
        sequence_obj = env["ir.sequence"]
        name_seq = "Stock Landed Cost of {}"
        for operating_unit in operating_unit_obj.search([]):
            lan_c_seq = sequence_obj.create(
                {
                    "name": name_seq.format(operating_unit.name),
                    "code": "stock.landed.cost.{}".format(operating_unit.code),
                    "prefix": "{}-LC".format(operating_unit.code),
                    "padding": 5,
                    "company_id": operating_unit.company_id.id,
                }
            )
            operating_unit.write({"stock_land_cost_sequence_id": lan_c_seq.id})
