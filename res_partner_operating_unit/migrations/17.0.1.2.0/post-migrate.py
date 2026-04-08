# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    if not version:
        return
    # Add missing index in operating_unit_partner_rel
    # Prior to this version, the pre_init_hook manually created the relation table,
    # bypassing the ORM's automatic creation, and so causing the indexes to be missing.
    # See: https://github.com/odoo/odoo/blob/7d146774c/odoo/fields.py#L4804-L4817
    #
    # The pre_init_hook is now removed, but we still need to create the index manually.
    cr.execute(
        """
        CREATE INDEX IF NOT EXISTS
        operating_unit_partner_rel_partner_id_operating_unit_id_idx
        ON operating_unit_partner_rel (partner_id, operating_unit_id)
        """
    )
