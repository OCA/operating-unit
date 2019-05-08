# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


""" This module exposes asumed knowledge over the runtime environment.
According to "Rather ask for forgiveness then permission", we expose a worldview
of the runtime instance model relationships and classify them according
to operating_unit model meta information. Then we try to overload those models
with the provided mixins. The graph override ensures this module is loaded last.
"""
from functools import wraps

from ._models import ModelBuildingEvictor

from odoo import models

def emit_operating_unit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].operating_unit_id:
            return func(*args, **kwargs)

        if 'operating_units' in args[0].env.context:
            operating_units = args[0].env.context['operating_units']
            operating_units |= args[0].operating_unit_id
            args[0] = args[0].with_context(operating_units=operating_units)
        return func(*args, **kwargs)
    return wrapper


##############################
# account
##############################

# Metadata
class AccountAccountOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.account', 'operating.unit.metadata.mixin']


class AccountTaxOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.tax', 'operating.unit.metadata.mixin']


class AccountTaxOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.journal', 'operating.unit.metadata.mixin']


# account.move -> account.move.line
class AccountMoveOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.move', 'operating.unit.independent.transaction.mixin']


class AccountMoveLineOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.move.line', 'operating.unit.dependent.transaction.mixin']
    _ou_follows = 'move_id'


# account.invoice -> account.invoice.line
# account.invoice -> account.invoice.tax
class AccountInvoiceOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.invoice', 'operating.unit.independent.transaction.mixin']

    action_move_create = emit_operating_unit(action_move_create)


class AccountInvoiceLineOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.invoice.line', 'operating.unit.dependent.transaction.mixin']
    _ou_follows = 'invoice_id'


class AccountInvoiceTaxOperatingUnit(models.Model, ModelBuildingEvictor):
    _inherit = ['account.invoice.tax', 'operating.unit.dependent.transaction.mixin']
    _ou_follows = 'invoice_id'
