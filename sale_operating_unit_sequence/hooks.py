# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import SUPERUSER_ID, api


def assign_ou_sequences(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        operating_unit_obj = env["operating.unit"]
        sequence_obj = env["ir.sequence"]
        for operating_unit in operating_unit_obj.search([]):
            sale_sequence = sequence_obj.create(
                {
                    "name": "Sale Order of {}".format(operating_unit.name),
                    "code": "sale.order.{}".format(operating_unit.code),
                    "prefix": "{}-SO".format(operating_unit.code),
                    "padding": 5,
                    "company_id": operating_unit.company_id.id,
                }
            )
            operating_unit.write({"sale_sequence_id": sale_sequence.id})
