##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import fields, models


class OperatingUnitExt(models.Model):

    _inherit = 'operating.unit'

    catchall_alias = fields.Char(string='Catchall alias')
    catchall_domain = fields.Char(string='Catchall domain')
    outgoing_mail_server_id = fields.Many2one(
        'ir.mail_server', string='Outgoing Mail Server')
