from . import stock_landed_cost

from odoo.addons.stock_landed_costs.models.stock_landed_cost \
    import LandedCost as LandedCost


def uninstall_hook(cr, registry):
    # If the method was patched we revert it during runtime
    if hasattr(LandedCost.button_validate, 'origin'):
        LandedCost._revert_method('button_validate')
