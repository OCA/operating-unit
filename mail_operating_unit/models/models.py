# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class BaseModel(models.AbstractModel):
    _inherit = "base"

    def _mail_get_operating_unit(self):
        """Retrieves the operating unit ID if it exists and is truthy.

        This method checks if the instance has the attribute
        either `operating_unit_id` or `operating_unit_ids`
        and whether it holds a truthy value.
        If both conditions are met, in case of `operating_unit_id`
        it returns the value of `operating_unit_id`.
        In case of `operating_unit_ids`, if exactly one operating unit is set,
        it returns the single record of the recordset.
        Otherwise, it returns `False`.
        """
        if "operating_unit_id" in self._fields and self.operating_unit_id:
            return self.operating_unit_id
        if "operating_unit_ids" in self._fields:
            operating_units = self.operating_unit_ids
            if (
                operating_units
                and len(operating_units) == 1
                and operating_units.alias_domain_id
            ):
                return operating_units
        return False

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

    def _mail_get_operating_unit_mail_server(self):
        """Return the operating unit outgoing mail server.

        Resolution rules:
        - use ``operating_unit_id.mail_server_id`` when available;
        - use the shared mail server from ``operating_unit_ids`` when all
          operating units point to the same one;
        - otherwise, if the current user's default operating unit belongs to
          ``operating_unit_ids`` and has a mail server, use it;
        - otherwise return ``False``.
        """
        self.ensure_one()
        if "operating_unit_id" in self._fields and self.operating_unit_id:
            return self.operating_unit_id.mail_server_id
        if "operating_unit_ids" in self._fields and self.operating_unit_ids:
            mail_servers = self.operating_unit_ids.mapped("mail_server_id")
            if mail_servers and len(mail_servers) == 1:
                return mail_servers

            default_operating_unit = self.env.user._get_default_operating_unit()
            if (
                default_operating_unit
                and default_operating_unit in self.operating_unit_ids
                and default_operating_unit.mail_server_id
            ):
                return default_operating_unit.mail_server_id

        return False

    def _mail_get_operating_unit_label(self):
        """Return operating unit label for logging purposes.

        Examples:
        - ``Operating Unit A`` for ``operating_unit_id``;
        - ``Operating Unit A, Operating Unit B`` for ``operating_unit_ids``;
        - ``no operating unit`` when no OU is set on the record.
        """
        self.ensure_one()
        if "operating_unit_id" in self._fields and self.operating_unit_id:
            return self.operating_unit_id.display_name
        if "operating_unit_ids" in self._fields and self.operating_unit_ids:
            return ", ".join(self.operating_unit_ids.mapped("display_name"))
        return "no operating unit"
