# Copyright 2019 - brain-tec AG
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        """ operating_unit_ids is defined also on the res.partner, and
            having two fields named equally on the 3rd type of inheritance
            doesn't propagate the values. Thus we do it manually.
        """
        res = super(ResUsers, self.with_context(
            copy_ou_to_partner=True)).create(vals)
        res.partner_id.operating_unit_ids = [
            (6, False, res.operating_unit_ids.ids)]
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """ operating_unit_ids is defined also on the res.partner, and
            having two fields named equally on the 3rd type of inheritance
            doesn't propagate the values. Thus we do it manually.
        """
        users = super(ResUsers, self.with_context(
            copy_ou_to_partner=True)).create(vals_list)
        for user in users:
            user.partner_id.operating_unit_ids = [
                (6, False, user.operating_unit_ids.ids)]
        return users

    @api.multi
    def write(self, vals):
        """ operating_unit_ids is defined also on the res.partner, and
            having two fields named equally on the 3rd type of inheritance
            doesn't propagate the values. Thus we do it manually.
        """
        res = super(ResUsers, self.with_context(
            copy_ou_to_partner=True)).write(vals)
        if 'operating_unit_ids' in vals:
            self.partner_id.operating_unit_ids = [
                (6, False, self.operating_unit_ids.ids)]
        return res
