# Copyright 2026 Jarsa (https://www.jarsa.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def uninstall_hook(env):
    """Restore the original domain of the operating unit access restriction."""
    access = env.ref(
        "operating_unit.ir_rule_operating_unit_allowed_operating_units",
        raise_if_not_found=False,
    )
    if access:
        access.write({"domain": "[('id','in',operating_unit_ids)]"})
