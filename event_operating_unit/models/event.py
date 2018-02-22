# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class Event(models.Model):

    _inherit = "event.event"

    @api.model
    def _default_operating_unit(self):
        return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=lambda self: self._default_operating_unit()
    )

    operating_unit_user_ids = fields.One2many(
        string='operating_unit Users',
        comodel_name='res.users',
        compute='_compute_operating_unit_user_ids',
        search='_search_operating_unit_user_ids'
    )

    @api.multi
    def _compute_operating_unit_user_ids(self):
        for record in self:
            result = self.env['res.users'].search(
                [('operating_unit_ids', 'in', self.operating_unit_id.ids)]
            )
            record.operating_unit_user_ids = result.ids

    def _search_operating_unit_user_ids(self, operator, value):
        result = self.env['res.users'].search(
            [('id', 'in', value)]
        )
        return [('operating_unit_id', 'in', result.operating_unit_ids.ids)]


class EventRegistraion(models.Model):

    _inherit = 'event.registration'

    operating_unit_id = fields.Many2one(
        string='Operating Unit',
        related='event_id.operating_unit_id',
        readonly=True
    )

    operating_unit_user_ids = fields.One2many(
        string='Operating Unit user ids',
        related='event_id.operating_unit_user_ids',
        readonly=True
    )


class EventSponsor(models.Model):

    _inherit = 'event.sponsor'

    operating_unit_id = fields.Many2one(
        string='Operating Unit',
        related='event_id.operating_unit_id',
        readonly=True
    )

    operating_unit_user_ids = fields.One2many(
        string='Operating Unit user ids',
        related='event_id.operating_unit_user_ids',
        readonly=True
    )


class EventTrack(models.Model):

    _inherit = 'event.track'

    operating_unit_id = fields.Many2one(
        string='Operating Unit',
        related='event_id.operating_unit_id',
        readonly=True
        )

    operating_unit_user_ids = fields.One2many(
        string='Operating Unit user ids',
        related='event_id.operating_unit_user_ids',
        readonly=True
        )
