# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import SUPERUSER_ID, api


def assign_ou_sequences(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        operating_unit_obj = env["operating.unit"]
        sequence_obj = env["ir.sequence"]
        for ou in operating_unit_obj.search([]):
            payment_sequence = sequence_obj.create(
                [
                    {
                        "name": "Payment Transfer of {}".format(ou.name),
                        "code": "account.payment.transfer.{}".format(ou.code),
                        "prefix": "{}-TRANS".format(ou.code),
                        "padding": 5,
                        "company_id": ou.company_id.id,
                    },
                    {
                        "name": "Payment Customer Invoice of {}".format(ou.name),
                        "code": "account.payment.customer.invoice.{}".format(ou.code),
                        "prefix": "{}-CUS.IN/".format(ou.code),
                        "padding": 5,
                        "company_id": ou.company_id.id,
                    },
                    {
                        "name": "Payment Customer Refund of {}".format(ou.name),
                        "code": "account.payment.customer.refund.{}".format(ou.code),
                        "prefix": "{}-CUS.OUT/".format(ou.code),
                        "padding": 5,
                        "company_id": ou.company_id.id,
                    },
                    {
                        "name": "Payment Suppier Invoice of {}".format(ou.name),
                        "code": "account.payment.supplier.invoice.{}".format(ou.code),
                        "prefix": "{}-SUPP.OUT/".format(ou.code),
                        "padding": 5,
                        "company_id": ou.company_id.id,
                    },
                    {
                        "name": "Payment Suppier Refund of {}".format(ou.name),
                        "code": "account.payment.supplier.refund.{}".format(ou.code),
                        "prefix": "{}-SUPP.IN/".format(ou.code),
                        "padding": 5,
                        "company_id": ou.company_id.id,
                    },
                ]
            )
            ou.write(
                {
                    "payment_transfer_seq_id": payment_sequence[0].id,
                    "payment_cust_inv_seq_id": payment_sequence[1].id,
                    "payment_cust_refund_seq_id": payment_sequence[2].id,
                    "payment_supp_inv_seq_id": payment_sequence[3].id,
                    "payment_supp_refund_seq_id": payment_sequence[4].id,
                }
            )
