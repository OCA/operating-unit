# Copyright 2018 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests.common import SavepointCase


class TestOperatiingUnitUserId(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ou1 = cls.env.ref('operating_unit.b2c_operating_unit')
        cls.ou2 = cls.env.ref('operating_unit.b2b_operating_unit')

        cls.user1 = cls.env['res.users'].with_context(
            no_reset_password=True,
            tracking_disable=True).create({
                'name': 'User 1',
                'login': 'user1',
                'email': 'user1@myhopefullynonexistingdomain.com',
                'operating_unit_ids': [(4, cls.ou1.id)]
            })

        cls.user2 = cls.env['res.users'].with_context(
            no_reset_password=True,
            tracking_disable=True).create({
                'name': 'User 2',
                'login': 'user2',
                'email': 'user2@myhopefullynonexistingdomain.com',
                'operating_unit_ids': [(4, cls.ou2.id)]
            })

        cls.user3 = cls.env['res.users'].with_context(
            no_reset_password=True,
            tracking_disable=True).create({
                'name': 'User 3',
                'login': 'user3',
                'operating_unit_ids': [(4, cls.ou1.id), (4, cls.ou2.id)]
            })

        cls.event1 = cls.env['event.event'].create({
            'name': 'Testevent',
            'operating_unit_id': cls.ou1.id,
            'date_begin': '2018-03-01 10:00:00',
            'date_end': '2018-03-01 11:00:00'
        })

        cls.event2 = cls.env['event.event'].create({
            'name': 'Testevent',
            'operating_unit_id': cls.ou2.id,
            'date_begin': '2018-03-01 10:00:00',
            'date_end': '2018-03-01 11:00:00'
        })

    def test_permission(self):
        events_user1 = self.env['event.event'].sudo(self.user1.id).search([])

        events_user2 = self.env['event.event'].sudo(self.user2.id).search([])
        events_user3 = self.env['event.event'].sudo(self.user3.id).search([])

        # we have one event in each ou.
        # user1 & user2 are assigned to one ou each
        self.assertEqual(len(events_user1), 1)
        self.assertEqual(len(events_user2), 1)
        # user3 is assigned to both
        self.assertEqual(len(events_user3), 2)

        # make sure we got the right one.
        self.assertEqual(events_user1, self.event1)
        self.assertEqual(events_user2, self.event2)
        self.assertIn(self.event1, events_user3)
        self.assertIn(self.event2, events_user3)

    def test_create_correct_ou(self):
        testevent = self.env['event.event'].sudo(self.user1.id).create({
            'name': 'Another Testevent',
            'operating_unit_id': self.ou1.id,
            'date_begin': '2018-03-01 10:00:00',
            'date_end': '2018-03-01 11:00:00'
        })
        self.assertEqual(len(testevent), 1)
        self.assertEqual(testevent.operating_unit_id, self.ou1)

    def test_change_ou(self):
        self.event1.sudo(self.user3.id).write(
            {'operating_unit_id': self.ou2.id}
        )
        self.assertEqual(self.event1.operating_unit_id, self.ou2)

    def test_drop_event(self):
        id_ = self.event1.id
        self.event1.sudo(self.user1.id).unlink()
        my_events = self.env['event.event'].search([('id', '=', id_)])
        self.assertEqual(len(my_events), 0)
