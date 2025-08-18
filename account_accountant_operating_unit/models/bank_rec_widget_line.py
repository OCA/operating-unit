##############################################################################
# Copyright (c) 2025 braintec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.0 (http://www.gnu.org/licenses/lgpl.html)
##############################################################################

from odoo import models


class BankRecWidgetLine(models.Model):
    _inherit = "bank.rec.widget.line"

    def _get_aml_values(self, **kwargs):
        return super()._get_aml_values(
            **kwargs,
            operating_unit_id=self.wizard_id.st_line_id.journal_id.operating_unit_id.id,
        )
