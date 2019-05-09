# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


""" This module exposes asumed knowledge over the runtime environment.
According to "Rather ask for forgiveness then permission", we expose a worldview
of the runtime instance model relationships and classify them according
to operating_unit model meta information. Then we try to overload those models
with the provided mixins. The graph override ensures this module is loaded last.
"""
from functools import wraps

from ._models import ModelBuildingEvictor as MBE

from odoo import models

# fmt: off
META = 'operating.unit.metadata.mixin'
ITX  = 'operating.unit.independent.transaction.mixin'
DTX  = 'operating.unit.dependent.transaction.mixin'

def emit_operating_unit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].operating_unit_id:
            return func(*args, **kwargs)

        if 'operating_units' in args[0].env.context:
            operating_units   = args[0].env.context['operating_units']
            operating_units  |= args[0].operating_unit_id
            args[0] = args[0].with_context(operating_units=operating_units)
        return func(*args, **kwargs)
    return wrapper


##############################
# account
##############################

# Metadata
class AccountAccount(    models.Model, MBE): _inherit = [META,'account.account'      ];
class AccountTax(        models.Model, MBE): _inherit = [META,'account.tax'          ];
class AccountTax(        models.Model, MBE): _inherit = [META,'account.journal'      ];
# account.move -> account.move.line
class AccountMove(       models.Model, MBE): _inherit = [ITX, 'account.move'         ];
class AccountMoveLine(   models.Model, MBE): _inherit = [DTX, 'account.move.line'    ]; _ou_follows = 'move_id';
# account.invoice -> account.invoice.line
# account.invoice -> account.invoice.tax
class AccountInvoice(    models.Model, MBE): _inherit = [ITX, 'account.invoice'      ];
AccountInvoice.action_move_create = emit_operating_unit(lambda self: super(type(self), self).action_move_create)
class AccountInvoiceLine(models.Model, MBE): _inherit = [DTX, 'account.invoice.line' ]; _ou_follows = 'invoice_id';
class AccountInvoiceTax( models.Model, MBE): _inherit = [DTX, 'account.invoice.tax'  ]; _ou_follows = 'invoice_id';

# fmt: on
