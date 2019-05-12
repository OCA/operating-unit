# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _

DOMAIN_TEMPLATE = (
    "['|',('{field}','=',False),"
    "     ('{field}','in', user.operating_unit_ids.ids)]"
)
RULE_NAME_TEMPLATE = (
    "Operating Unit: restrict access on {model._description} "
    "(autogenerated, but adaptable)"
)
RULE_XMLID_TEMPLATE = (
    "operating_unit.ir_rule_allowed_operating_unit_for_{model._table}"
)

AUTOMATED_VIEW_TYPES = [
    'tree',
    'form',
    # 'search',  # TODO: It's a little more difficult.
]

VIEW_TEMPLATE = """
<data>
    <xpath expr="{xpath}" position="after">
        <field  name="{field}"
                widget="{widget}"
                invisible="{inivisble}"
                <!-- domain is infered from python code -->
                options="{'no_create': True, 'color_field': 'color'}"/>
    </xpath>
</data>
"""

VIEW_NAME_TEMPLATE = (
    "{inherited_view.name} operating.unit overloaded"
)
VIEW_XMLID_TEMPLATE = (
    "operating_unit.{inherited_view.xmlid}_operating_unit"
)


class Container(object):
    pass


# TODO: Also reconcile on installing new modules to ensure consistent state!

class OperatingUnitIrModel(models.Model):
    _inherit = 'ir.model'

    def _compute_has_company_id(self):
        for model in self:
            model.has_company_id = bool(
                model.field_id.filtered(lambda f: f.name == 'company_id'))

    has_company_id = fields.Boolean(
        compute='_compute_has_company_id',
        help="For client side view rendering")

    operating_unit_enabled = fields.Boolean(
        readonly = True,
        default = False,
        help="Denotes if operating units are enabled on this model. This means "
             "Access Rules are in place and inheriting views exposing the "
             "respective fields are active."
    )

    def toggle_operating_unit(self):
        self._toggle_operating_unit_ir_rule(not self.operating_unit_enabled)
        self._toggle_operating_unit_ir_ui_view(not self.operating_unit_enabled)
        self.operating_unit_enabled = not self.operating_unit_enabled

    def _toggle_operating_unit_ir_rule(self, active=True):
        model = self.env[self.name]
        if getattr(model, '_ou_metadata', None):
            field = 'operating_unit_ids'
        elif getattr(model, '_ou_transaction', None):
            field = 'operating_unit_id'
        else:
            # We should never reach to this point (by design)
            raise "This should be only called on OU enabled models"

        new_rule = Container()
        new_rule.xmlid = RULE_XMLID_TEMPLATE.format(**locals())

        existing = self.env.ref(xmlid, raise_if_not_found=False)
        if existing:
            if existing.active != active:
                existing.toggle_active()
            return

        new_rule.domain = DOMAIN_TEMPLATE.format(**locals())
        new_rule.name = RULE_NAME_TEMPLATE.format(**locals())
        new_rule.model_id = self.env['ir.model'].search(['name', '=', model._name])

        new_rule.res_id = self.env['ir.rule'].create({
            # fmt: off
            'model_id'     : new_rule.model_id.id,
            'domain_force' : new_rule.domain,
            'name'         : new_rule.name,
            'global'       : True,
            'active'       : active,
            'perm_unlink'  : True,
            'perm_write'   : True,
            'perm_read'    : True,
            'perm_create'  : True,
            # fmt: on
        }).ensure_one()
        self.env['ir.model.data']._update_xmlids([{
            'xml_id': new_rule.xmlid,
            'record': new_rule.res_id,
        }])


    def _toggle_operating_unit_ir_ui_view(self, active=True):
        model = self.env[self.name]

        if getattr(model, '_ou_metadata', None):
            field = 'operating_unit_ids'
            widget = 'many2many_tags'
        elif getattr(model, '_ou_transaction', None):
            field = 'operating_unit_id'
            widget = ''
        else:
            # We should never reach to this point (by design)
            raise "This should be only called on OU enabled models"

        model_id = self.env['ir.model'].search(['name', '=', model._name])
        for view in model_id.view_ids.filtered(
            lambda v: v.type in AUTOMATED_VIEW_TYPES and v.mode == 'primary'):
            inherited_view = Container()
            inherited_view.name = view.name
            inherited_view.xmlid = view.get_external_id().values()[0]

            new_view = Container()
            new_view.xmlid = VIEW_XMLID_TEMPLATE.format(**locals())

            existing = self.env.ref(new_view.xmlid, raise_if_not_found=False)
            if existing:
                if existing.active != active:
                    existing.toggle_active()
                return

            inivisble = 0  # TODO: lxml analyze inherited view ocurrence
            xpath = "//field[@name='company_id']"  # TODO: same for xpath, I guess.
            new_view.arch = VIEW_TEMPLATE.format(**locals())
            new_view.name = VIEW_NAME_TEMPLATE.format(**locals())

            new_view.res_id = self.env['ir.ui.view'].create({
                # fmt: off
                'name'       : new_view.name,
                'arch'       : new_view.arch,
                'model'      : view.model,
                'type'       : view.type,
                'inherit_id' : view.id,
                'mode'       : 'extension',
                'active'     : active,
                'group_id'   : view.group_id,  # TODO: Enforce group at this level?
                # fmt: on
            }).ensure_one()
            self.env['ir.model.data']._update_xmlids([{
                'xml_id': new_view.xmlid,
                'record': new_view.res_id,
            }])
