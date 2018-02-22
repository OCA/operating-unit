# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
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
                'operating_unit_ids': [(4, cls.ou1.id)]
            })

        cls.user2 = cls.env['res.users'].with_context(
            no_reset_password=True,
            tracking_disable=True).create({
                'name': 'User 2',
                'login': 'user2',
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

    def test_compute(self):
        users = self.event1.operating_unit_user_ids
        # The demo user is in all ous so we have 3 instead of 2
        self.assertEqual(len(users), 3)
        # We should find user1 which is only in ou 1 and user3
        # which is in both.
        self.assertIn(self.user1, users)
        self.assertIn(self.user3, users)
        # But user2 doesn't belong to our orgunit
        self.assertNotIn(self.user2, users)

        users = self.event2.operating_unit_user_ids
        # The demo user is in all ous so we have 3 instead of 2
        self.assertEqual(len(users), 3)

        # In ou2 we have user2 & user3
        self.assertIn(self.user2, users)
        self.assertIn(self.user3, users)
        # But we don't have user1
        self.assertNotIn(self.user1, users)

    def test_search(self):
        events_user1 = self.env['event.event'].search(
            [('operating_unit_user_ids', 'in', self.user1.ids)]
        )

        events_user2 = self.env['event.event'].search(
            [('operating_unit_user_ids', 'in', self.user2.ids)]
        )
        events_user3 = self.env['event.event'].search(
            [('operating_unit_user_ids', 'in', self.user3.ids)]
        )

        # we have one event in each ou.
        # user1 & user2 are assigned to one ou each
        self.assertEqual(len(events_user1), 1)
        self.assertEqual(len(events_user2), 1)
        # user3 is assigned to both
        self.assertEqual(len(events_user3), 2)

        # make sure we got the right one.
        self.assertEqual(events_user1[0], self.event1)
        self.assertEqual(events_user2[0], self.event2)
        self.assertIn(self.event1, events_user3)
        self.assertIn(self.event2, events_user3)
