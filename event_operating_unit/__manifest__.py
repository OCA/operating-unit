# Copyright 2018 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Event Operating Unit',
    'version': '11.0.1.0.0',
    'category': 'others',
    'license': 'LGPL-3',
    'author': 'camptocamp, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/operating_unit',
    'depends': [
        'event',
        'operating_unit',
        'website_event_track',
    ],
    'data': [
        'views/event_views.xml',
        'views/event_track_views.xml',
        'views/event_registration_views.xml',
        'views/event_sponsor_views.xml',
        'security/event_operating_security.xml',
    ],
    'installable': True,
}
