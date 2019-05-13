# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


""" This module exposes asumed knowledge over the runtime environment.
According to "Rather ask for forgiveness then permission", we expose a worldview
of the runtime instance model relationships and classify them according
to operating_unit model meta information. Then we try to overload those models
with the provided mixins. The graph override ensures this module is loaded last.
"""
from functools import wraps

from odoo.addons.base_transversal_module import ModelBuildingEvictor as MBE

from odoo import models, fields

# fmt: off
META = 'operating.unit.metadata.mixin'
ITX  = 'operating.unit.independent.transaction.mixin'


#### ========================================= ####
#### Wrappers to overload function             ####
#### ========================================= ####

def emit_operating_unit(func_getter):
    """ Context sentinel payload emitted on "outgoing" transitions.
    This is catched by the create method of subsequent transactional
    records created during the current server transaction.

    Multiple values trigger a user facing dialogue to resolve the confilct. """

    @wraps(func_getter)
    def wrapper(*args, **kwargs):
        if not args[0].operating_unit_id:
            return func_getter(args[0])(*args[1:], **kwargs)

        if 'operating_units' in args[0].env.context:
            operating_units   = args[0].env.context['operating_units']
            operating_units  |= args[0].operating_unit_id
        else:
            operating_units   = args[0].operating_unit_id
        args = list(args)
        args[0] = args[0].with_context(operating_units=operating_units)
        return func_getter(args[0])(*args[1:], **kwargs)
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
        func_getter = lambda self: getattr(super(klass, self), method)
        setattr(klass, method, emit_operating_unit(func_getter))
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
# account & friends
##############################
_meta('account.account')
_meta('account.tax')
_meta('account.journal')
_inTX('account.move')
_deTX('account.move.line', 'move_id')
_inTX('account.invoice', ['action_move_create'])
_deTX('account.invoice.line', 'invoice_id')
_deTX('account.invoice.tax', 'invoice_id')
_meta('account.analytic.account')
_meta('account.analytic.group')
_inTX('account.analytic.line')
_meta('account.asset.category')
_inTX('account.asset.asset')
_inTX('account.bank.statement')
_deTX('account.bank.statement.line', 'statement_id')
_inTX('account.voucher')
_deTX('account.voucher.line', 'voucher_id')
_meta('account.fiscal.position')
_inTX('account.payment')
_meta('account.payment.term')
_meta('account.reconcile.model')
_meta('account.budget.post')
_inTX('crossovered.budget')
_deTX('crossovered.budget.lines', 'crossovered_budget_id')
# account.abstract.payment
# account.analytic.tag
# account.financial.html.report
# account.fiscal.year
# account.invoice.report
# account.online.provider
# account.partial.reconcile - probably never: allow reconciliation between OUs
# account.report.manager
# asset.asset.report


##############################
# partner & products
##############################
_meta('res.partner')
_meta('product.product')
_meta('product.template')
_meta('product.pricelist')
# product.price.history
# product.pricelist.item
# product.supplierinfo


##############################
# sale, purchase & friends
##############################
_inTX('sale.order')
_deTX('sale.order.line', 'order_id')
# sale.report
_inTX('pruchase.order')
_deTX('purchase.order.line', 'order_id')
# purchase.bill.union
# purchase.report
_meta('crm.team')
_inTX('crm.lead')
# crm.activity.report


##############################
# hr
##############################
_meta('hr.employee')
_meta('hr.department')  # At times departments overlap with operating units
_meta('hr.job')
_meta('hr.leave.type')
_meta('hr.payroll.structure')
_meta('hr.salary.rule')
_meta('hr.salary.rule.category')
_inTX('hr.applicant')
_inTX('hr.contract')
_inTX('hr.payslip')
_deTX('hr.payslip.line', 'slip_id')
# hr.expense
# hr.expense.sheet - How to? coerce to hr.expense once assigned -> readonly
# hr.contribution.register - Necesary to place under operating units? -> meta


##############################
# stock
##############################
_meta('stock.location')
_meta('stock.warehouse')
_inTX('stock.inventory')
_deTX('stock.inventory.line', 'inventory_id')
_inTX('stock.landed.cost')
_inTX('stock.picking')
# TODO: stock.move mostly has pickings, but some don't. Check!
_deTX('stock.move', 'picking_id')
# stock.quant - Does it make sense? Already heavily namespaced by locations
# stock.quant.package - Same here.
# stock.location.route
# stock.report
# stock.rule
# stock.warehouse.orderpoint - Does it make sense? Controlled by cron. New dependent meta required?


##############################
# mrp & friends
##############################
_meta('mrp.bom')
_meta('mrp.workcenter')
_meta('mrp.routing')
_inTX('mrp.production')
# mrp.document
# mrp.eco
# mrp.routing.workcenter

_meta('maintenance.team')
_inTX('maintenance.request')
# maintenance.equipment
# maintenance.equipment.category

_meta('quality.alert.team')
# quality.alert
# quality.check
# quality.point


##############################
# project
##############################

_meta('project.project')
_inTX('project.task')

# delivery.carrier
# digest.digest
# fleet.vehicle
# iap.account
# payment.acquirer
# pos.config
# pos.order
# pos.order.line
# report.all.channels.sales
# report.pos.order
# report.project.task.user
# report.stock.forecast
# res.currency.rate
# res.partner.bank
# res.users
# resource.calendar
# resource.calendar.leaves
# resource.mixin
# resource.resource
# resource.test
# snailmail.letter
# website


# Is it true that ...
_deTX('thirsty.camels.rock', 'invoice_ids')

# fmt: on
