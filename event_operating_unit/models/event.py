# Copyright 2018 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class Event(models.Model):

    _inherit = 'event.event'

    @api.model
    def _default_operating_unit(self):
        return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=lambda self: self._default_operating_unit()
    )


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    operating_unit_id = fields.Many2one(
        string='Operating Unit',
        related='event_id.operating_unit_id',
        readonly=True,
        store=True
    )


class EventSponsor(models.Model):

    _inherit = 'event.sponsor'

    operating_unit_id = fields.Many2one(
        string='Operating Unit',
        related='event_id.operating_unit_id',
        readonly=True,
        store=True
    )


class EventTrack(models.Model):

    _inherit = 'event.track'

    operating_unit_id = fields.Many2one(
        string='Operating Unit',
        related='event_id.operating_unit_id',
        readonly=True,
        store=True
    )
