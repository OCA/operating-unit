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

from odoo import models, fields

# fmt: off
META = 'operating.unit.metadata.mixin'
ITX  = 'operating.unit.independent.transaction.mixin'


#### ========================================= ####
#### Wrappers to overload function             ####
#### ========================================= ####

def emit_operating_unit(func):
    """ Context sentinel payload emitted on "outgoing" transitions.
    This is catched by the create method of subsequent transactional
    records created during the current server transaction.

    Multiple values trigger a user facing dialogue to resolve the confilct. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].operating_unit_id:
            return func(*args, **kwargs)

        if 'operating_units' in args[0].env.context:
            operating_units   = args[0].env.context['operating_units']
            operating_units  |= args[0].operating_unit_id
            args[0] = args[0].with_context(operating_units=operating_units)
        else:
            args[0] = args[0].with_context(operating_units=args[0].operating_unit_id)

        return func(*args, **kwargs)
    return wrapper


def set_up_related_operating_unit_id(cls, follows_field):
    """ Field setter for Operating Unit for dependent transactional data which
    is guaranteed to always adopt the operating unit of another transaction.
    Raison d'etre: We need to set composable (!) operating_unit_id related
    fields at python load time to be already set up at odoo load time. """
    operating_unit_id = fields.Many2one(
        'operating.unit',
        string="Operating Unit",
        # We need to set this at class instanciation time,
        # on inherited classes. Therefore this indirection.
        related=follows_field + '.operating_unit_id',
        store=True  # For reporting, speed
        # Defaults to readonly, which is intended.
    )
    setattr(cls, 'operating_unit_id', operating_unit_id)
    # See mixins: it's classified as transactional data
    setattr(cls, '_ou_transaction', True)


#### ========================================= ####
#### Factories to keep this file slick as hell ####
#### ========================================= ####

# _mro_tuple = (MBE, models.Model)

# Independent Transaction
def _inTX(inh, emitting_method_names=tuple()):
    name = inh.replace('.', '_')
    klass = type(name, (MBE, models.Model), {
        '__module__': __name__, '_inherit': [ITX, inh], '_name': inh})
    for method in emitting_method_names:
        setattr(
            klass, method,
            emit_operating_unit(
                lambda self: getattr(
                    super(type(self), self),
                    method)))
    return klass

# Dependent Transaction
def _deTX(inh, field_name):
    name = inh.replace('.', '_')
    klass = type(name, (MBE, models.Model), {
        '__module__': __name__, '_inherit': [inh]})
    set_up_related_operating_unit_id(klass, field_name)
    return klass

# Metadata
def _meta(inh):
    name = inh.replace('.', '_')
    klass = type(name, (MBE, models.Model), {
        '__module__': __name__, '_inherit': [META, inh], '_name': inh})
    return klass


##############################
# account
##############################
_meta('account.account')
_meta('account.tax')
_meta('account.journal')
_inTX('account.move')
_deTX('account.move.line', 'move_id')
_inTX('account.invoice', ['action_move_create'])
_deTX('account.invoice.line', 'invoice_id')
_deTX('account.invoice.tax', 'invoice_id')

# Is it true that ...
_deTX('thirsty.camels.rock', 'invoice_ids')

# fmt: on
