# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = "pos.config"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
    )

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Company in the POS Config "
                        "and in the Operating Unit must be the same."
                    )
                )

    @api.constrains("operating_unit_id", "invoice_journal_id")
    def _check_invoice_journal_operating_unit(self):
        for rec in self:
            if (
                rec.invoice_journal_id
                and rec.operating_unit_id
                and rec.invoice_journal_id.operating_unit_id != rec.operating_unit_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Operating Unit in the Invoice Journal"
                        " and in the POS Config must be the same."
                    )
                )

    @api.constrains("operating_unit_id", "journal_id")
    def _check_journal_operating_unit(self):
        for rec in self:
            if (
                rec.journal_id
                and rec.operating_unit_id
                and rec.journal_id.operating_unit_id != rec.operating_unit_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Operating Unit in the POS Journal"
                        " and in the POS Config must be the same."
                    )
                )

    @api.constrains("operating_unit_id", "picking_type_id")
    def _check_picking_type_operating_unit(self):
        for rec in self:
            warehouse = rec.picking_type_id.warehouse_id
            if (
                warehouse.operating_unit_id
                and rec.picking_type_id
                and rec.operating_unit_id
                and warehouse.operating_unit_id != rec.operating_unit_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Operating Unit in the Picking Type"
                        "Warehouse and in the POS Config must be the same."
                    )
                )
