# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderQuote(models.Model):
    _name = 'sale.order.quote'
    _description = 'Internal Quote'

    name = fields.Char(string='Name')
    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        required=True
    )
    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead',
        readonly=True
    )
    line_ids = fields.One2many(
        'sale.order.quote.line', 'quote_id', string='Products')
    state = fields.Selection([
        ('new', 'New'),
        ('sent', 'Sent'),
        ('received', 'Received')], string='State',
        copy=False, default='new', track_visibility='onchange')

    _sql_constraints = [
        ('sale_order_quote_operating_unit_uniq',
         'unique (sale_id, operating_unit_id)',
         _("You can only have one internal quote per operating unit and "
           "sale order!")),
    ]

    notes = fields.Text('Notes')
    expected_date = fields.Date(string="Expected Date")

    assigned_to = fields.Many2one('res.users', related='lead_id.user_id')

    @api.multi
    @api.constrains('operating_unit_id')
    def _check_operating_unit_id(self):
        for rec in self:
            if rec.operating_unit_id == rec.sale_id.operating_unit_id:
                raise UserError(_(
                    "You cannot create an internal quote for the same "
                    "operating unit as the sale order!"))

    @api.onchange('operating_unit_id')
    def _onchange_operating_unit_id(self):
        if self.operating_unit_id:
            sale_id = self.env['sale.order'].browse(
                self._context.get('active_id'))
            self.name = sale_id.name or 'New' + ' - ' + self.\
                operating_unit_id.code

    def generate_lead_description(self):
        Template = self.env["mail.template"]
        description = Template.with_context()._render_template(
            self.sale_id.company_id.lead_description_template,
            "sale.order.quote", self.id)
        return description

    def generate_lead_description(self):
        Template = self.env["mail.template"]
        description = Template.with_context()._render_template(
            self.sale_id.company_id.lead_description_template,
            "sale.order.quote", self.id)
        return description

    def prepare_crm_lead_values(self):
        teams = self.env['crm.team'].sudo().search([
            ('operating_unit_id', '=', self.operating_unit_id.id)
        ], limit=1)
        if not teams:
            raise UserError(_("This operating unit has no sales team! Please "
                              "consider creating one."))
        description = self.generate_lead_description()
        return {
            'name':
                self.sale_id.name + ' - ' + self.operating_unit_id.code,
            'partner_id': self.env.user.partner_id.id,
            'type': 'opportunity',
            'description': description,
            'user_id': False,
            'team_id': teams[0].id,
            'date_deadline': self.expected_date
        }

    def generate_crm_lead(self):
        for rec in self:
            if not rec.lead_id:
                rec.lead_id = self.env['crm.lead'].sudo().create(
                    rec.prepare_crm_lead_values())
        return True

    def action_send(self):
        return self.write({'state': 'sent'})

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get('expected_date', False) and self.lead_id:
            self.lead_id.date_deadline = vals.get('expected_date')
        if vals.get('state', False) == 'sent':
            for rec in self:
                rec.generate_crm_lead()
        return res
