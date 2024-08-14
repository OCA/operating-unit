# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class BaseModel(models.AbstractModel):
    _inherit = "base"

    def _mail_get_operating_unit(self):
        """Retrieves the operating unit ID if it exists and is truthy.

        This method checks if the instance has the attribute `operating_unit_id`
        and whether it holds a truthy value.
        If both conditions are met, it returns the value of `operating_unit_id`.
        Otherwise, it returns `False`.
        """
        return (
            self.operating_unit_id
            if "operating_unit_id" in self and self.operating_unit_id
            else False
        )

    def _mail_get_operating_units(self):
        """Retrieve the operating unit (OU) based on specific criteria.

        The process is as follows:

        1. Return the OU associated with the current record, if any.
        2. If not, fetch the OUs associated with the current user.
        3. If the user has no OUs, return False.
        4. If the user has exactly one OU, return it.
        5. If the user has multiple OUs and they share a single alias domain,
           return the first OU that has that alias domain.
        6. If none of these conditions are met, return False.
        """
        self.ensure_one()

        operating_unit = self._mail_get_operating_unit()
        if operating_unit:
            return operating_unit

        user = self.env.user
        user_operating_units = user.operating_unit_ids

        if not user_operating_units:
            return False

        if len(user_operating_units) == 1:
            return user_operating_units

        if len(user_operating_units) > 1:
            alias_domains = user_operating_units.mapped("alias_domain_id")
            if len(alias_domains) == 1:
                return next(
                    (unit for unit in user_operating_units if unit.alias_domain_id),
                    False,
                )

        return False

    def _mail_get_alias_domains(self, default_company=False):
        # Use operating unit's alias domain, if any.
        # If an OU is associated with a record, its alias domain is used.
        # Otherwise, the default alias domain is applied.
        alias_domains = super()._mail_get_alias_domains(default_company=default_company)
        return {
            record.id: (
                operating_units.alias_domain_id
                if (operating_units := record._mail_get_operating_units())
                else alias_domains[record.id]
            )
            for record in self
        }
