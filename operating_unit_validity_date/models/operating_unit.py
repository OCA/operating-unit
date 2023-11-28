import datetime

from odoo import fields, models

SOON_EXPIRE_DAYS = 30


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    valid_from = fields.Date("Valid From")
    valid_until = fields.Date("Valid Until")
    validity_state = fields.Selection(
        [
            ("expired", "Expired"),
            ("soon_expire", "Soon to Expire"),
            ("valid", "Valid"),
            ("not_valid_yet", "Not Valid Yet"),
        ],
        compute="_compute_valid_state",
    )

    def _compute_valid_state(self):
        today = datetime.date.today()
        for record in self:
            if record.valid_until and record.valid_until < today:
                record.validity_state = "expired"
            elif record.valid_from and record.valid_from > today:
                record.validity_state = "not_valid_yet"
            elif (
                record.valid_until
                and (record.valid_until - today).days < SOON_EXPIRE_DAYS
            ):
                record.validity_state = "soon_expire"
            else:
                record.validity_state = "valid"
