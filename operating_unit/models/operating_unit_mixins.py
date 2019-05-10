# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


VIEW_DOMAIN = "[('user_ids', '=', uid), ('company_id', '=', 'company_id')]"
WITHOUT_COMPANY_ERROR = (
    "An Operating Unit can only be set on records that also "
    "have a company set (strict company namespacing)."
    "Record {rec.display_name} has no company set."
)
NOT_SAME_COMPANY_ERROR = (
    "The Operating Unit must be of the same company as the "
    "record (company namespacing). Record {rec.display_name} has company "
    "{rec.company_id.display_name} but it's operating unit {unit.display_name} "
    "belongs to company {unit.company_id.display_name}."
)
TRANSACTION_REALM_BOUNDARIES_ERROR = (
    "All bound metadata must share the operating unit of this transaction. "
    "The record {rec.display_name} related on field {field.string} doesn't "
    "share the operating unit of this transaction ({self.display_name})."
)
METADATA_NO_SHARED_REALM = (
    "Linked and bound metadata must share at least one operating unit."
    "The record {rec.display_name} related on field {field.string} doesn't "
    "share an operating unit with this metadata ({self.display_name})."
)


class OperatingUnitRealmEnsurer(object):
    """
    Each record (metadata or transactional) knows two basic states, which are
    enforced accordingly:
     - "Bound" to one or more operating units
     - "Unbound" without any operating unit (= globally available)

    Bound records can be related to any unbound or to bound records which have
    a common operating unit.

    Unbound records can relate to any other record.
    """

    def _ensure_operating_unit_realm(self):
        """ Ensures realm boundaries of operating units. All "participating"
        records (transactional or metadata) must be either unbound or share at
        least one common operating unit.

        Yet an existing transaction, can passively be "expulsed" of a realm if
        one of it's linked metadata's operating units are modified and would
        stop sharing one with the transaction.

        "Expulsed" transaction block on write, unless their realm boundary is
        healed or they are made unbound.

        TODO: Ensure through SQL queries that transactions that would be
        expulsed are shown with a warning + confirmation (with the possibility
        for the user to make them unbound)
        """

        # In the context of a transaction ...
        if getattr(self, '_ou_transaction', None):

            # If no operating_unit_id is set, it's an unbound transaction.
            # Don't enforce realms on unbound transactions!
            if not self.operating_unit_id:
                return
            operating_units = self.operating_unit_id
            ERROR_MSG = TRANSACTION_REALM_BOUNDARIES_ERROR

        # In the context of metadata ...
        elif getattr(self, '_ou_metadata', None):
            # If no operating_unit_ids is set, it's an unbound metadata.
            # Don't enforce realms on unbound metadata!
            if not self.operating_unit_ids:
                return
            operating_units = self.operating_unit_ids
            ERROR_MSG = METADATA_NO_SHARED_REALM

        else:
            raise "This class was wrongly inherited."

        _rel_metadata_field_names = self._get_rel_metadata_field_names()

        # Check that all related metadata record (if any) shares at least one
        # operating unit with this record or otherwise is an unbound
        # metadata record with no operating unit set at all (which is
        # bypassed for the check)
        for fieldname, field in _rel_metadata_field_names:
            rec = getattr(self, fieldname)
            if not rec or not rec.operating_unit_ids:
                # An unbound record, not elibile for realm enforcement
                continue
            if not (operating_units & rec.operating_unit_ids):
                raise ValidationError(_(ERROR_MSG).format(
                    rec=rec, field=field, self=self))

    def _get_rel_metadata_field_names(self):
        """ Get all fields that relate to a model, which has operating units.
        The '_ou_metadata' attribute tells us, if a model has operating units.

        returns: {(field_name, fiel_obj), ...} """
        return {
            (n, f) for n, f in self._fields.items()
            if (
                f.relational and
                getattr(self.env[f.comodel_name], '_ou_metadata', None)
            )
        }

    @api.model
    def create(self, vals):
        self._ensure_operating_unit_realm()
        # TODO: Check if this style super call selects the right object in the MRO
        return super().write(vals)

    @api.multi
    def write(self, vals):
        # Only check if some "suspect" field is written on.
        # Evicting a whole class access errors if a user modifies a record
        # but hasn't read access to the metadata as long as no metadata is
        # modified. Just some improvable heuristics...
        field_names = {n for (n, f) in self._get_rel_metadata_field_names()}
        if any(k for k in vals.keys() if k in field_names):
            self._ensure_operating_unit_realm()
        # TODO: Check if this style super call selects the right object in the MRO
        return super().write(vals)


class OperatingUnitMetadataMixin(models.AbstractModel, OperatingUnitRealmEnsurer):
    """
    Operating Unit Mixin for metadata. Metadata can be configured
    transversal and belong to multiple operating units.

    Note on strict namespacing: Can intentionally only be used on models which
    exhibit company_id field.
    """
    _name = 'operating.unit.metadata.mixin'
    _description = "Operating Unit Mixin for Metadata"

    # It's a metadata model
    _ou_metadata = True

    def _init_(self, pool, cr):
        """ Just assert certain things are given. This is called at the end of
        the models.BaseModel._build_model classmethod (for "backwards
        compatibility", it says). """
        assert 'company_id' in self._fields, (
            "The field 'company_id' needs to be present on the model for "
            "the OperatingUnitMetadataMixin")

        # In case user_id is not present remove the
        # onchange function alltogether
        if 'user_id' not in self._fields:
            del(self._onchange_user_operating_units)


    operating_unit_ids = fields.Many2many(
        'operating.unit',
        string='Operating Units',
        domain=VIEW_DOMAIN,
        default=lambda self: self._operating_units_default_get()
    )

    def _operating_units_default_get(self):
        """ units (sic!). Infer the default operating units through
        the assigned user or, as a fall back, the current user. """
        if getattr(self, 'user_id', None):
            # It might be the secretary recording a document for a sales person
            # take the default from the document "owner" (user_id)
            defaults = self.sudo(self.user_id).env['ir.default'].get_model_defaults(self._name)
            if 'operating_unit_ids' in defaults:
                return defaults.get('operating_unit_ids')
        return self.env.user.operating_units_default_get()

    @api.multi
    @api.constrains('operating_unit_ids', 'company_id')
    def _check_company_operating_unit(self):
        """ Enforce operating unit is of the same company as the current record.
        Also enforce that current record without company cannot be part of an
        operating unit (strong namespacing through company). """
        for rec in self.filtered('operating_unit_ids'):
            if not rec.company_id:
                raise ValidationError(_(WITHOUT_COMPANY_ERROR).format(rec=rec))
            offending_units = rec.operating_unit_ids.filtered(
                lambda u: u.company_id != rec.company_id)
            if not offending_units:
                continue
            raise ValidationError(_(NOT_SAME_COMPANY_ERROR ).format(
                # Simplification: just advise the first operating unit
                rec=rec, unit=offending_units[0],
            ))

    @api.onchange('company_id')
    def _onchange_company_operating_units(self):
        """ Ensures strict company name spacing by removing OUs if company is
        removed. """
        self.ensure_one()
        if not self.company_id and self.operating_unit_ids:
            # We reset the operating units.
            self.operating_unit_ids = False


    # Will emit a WARNING log, if no `user_id` is present on the cls
    # otherwise it will just get ignored. Wait no: see _init_()
    @api.onchange('user_id')
    def _onchange_user_operating_units(self):
        """ Ensures a user change triggers the defaulting logic on
        transactional models. """
        self.ensure_one()
        self.operating_unit_id = self._operating_units_default_get()


class OperatingUnitIndependentTansactionMixin(models.AbstractModel, OperatingUnitRealmEnsurer):
    """ Operating Unit Mixin for independent transactional data, which is not
    guaranteed to always adopt the operating unit of another transaction.

    Note on strict namespacing: Can intentionally only be used on models which
    exhibit company_id field.
    """
    _name = 'operating.unit.independent.transaction.mixin'
    _description = "Operating Unit Mixin for Independent Transactions"

    # It's a transactional model
    _ou_transaction = True

    def _init_(self, pool, cr):
        """ Just assert certain things are given. This is called at the end of
        the models.BaseModel._build_model classmethod (for "backwards
        compatibility", it says). """
        assert 'company_id' in self._fields, (
            "The field 'company_id' needs to be present on the model for "
            "the OperatingUnitIndependentTansactionMixin")

        # In case user_id is not present remove the
        # onchange function alltogether
        if 'user_id' not in self._fields:
            del(self._onchange_user_operating_unit)


    operating_unit_id = fields.Many2one(
        'operating.unit',
        string="Operating Unit",
        domain=VIEW_DOMAIN,
        default=lambda self: self._operating_unit_default_get()
    )

    def _operating_unit_default_get(self):
        """ unit (sic!). Infer the single default operating unit through
        the assigned user or, as a fall back, the current user. """
        if getattr(self, 'user_id', None):
            # It might be the secretary recording a document for a sales person
            # take the default from the document "owner" (user_id)
            defaults = self.sudo(self.user_id).env['ir.default'].get_model_defaults(self._name)
            if 'operating_unit_id' in defaults:
                return defaults.get('operating_unit_id')
        return self.env.user.operating_unit_default_get()

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        """ Enforce operating unit is of the same company as the current record.
        Also enforce that current record without company cannot be part of an
        operating unit (strong namespacing through company). """
        for rec in self.filtered('operating_unit_id'):
            if not rec.company_id:
                raise ValidationError(_(WITHOUT_COMPANY_ERROR).format(rec=rec))
            if rec.operating_unit_id.company_id == rec.company_id:
                continue
            raise ValidationError(_(NOT_SAME_COMPANY_ERROR ).format(
                rec=rec, unit=rec.operating_unit_id,
            ))

    @api.onchange('company_id')
    def _onchange_company_operating_unit(self):
        """ Ensures strict company name spacing by removing OU if company is
        removed. """
        self.ensure_one()
        if not self.company_id and self.operating_unit_id:
            # We reset the operating unit.
            self.operating_unit_id = False

    # Will emit a WARNING log, if no `user_id` is present on the cls
    # otherwise it will just get ignored. Wait no: see _init_()
    @api.onchange('user_id')
    def _onchange_user_operating_unit(self):
        """ Ensures a user change triggers the defaulting logic on
        transactional models. """
        self.ensure_one()
        self.operating_unit_id = self._operating_unit_default_get()


    def create(self, vals):
        if not 'operating_units' in self.env.context or not self.env.context['operating_units']:
            return super().create(vals)

        operating_units = self.env.context['operating_units']

        assert isinstance(operating_units, models.BaseModel), "We asked for a RecordSet, dude!"

        if len(operating_units) == 1:
            vals['operating_unit_id'] = operating_units[0].id
            return super().create(vals)
        else:
            if getattr(therading.current_thread(), 'type', None) == 'cron':
                return super().create(vals)
            # TODO: Implement a js dialog to manually select the target Operating Unit
            # For now: dummy assign the first one passed
            vals['operating_unit_id'] = operating_units[0].id
            return super().create(vals)



class OperatingUnitDependentTansactionMixin(models.AbstractModel):
    """ Operating Unit Mixin for dependent transactional data which is
    guaranteed to always adopt the operating unit of another transaction. """
    _name = 'operating.unit.dependent.transaction.mixin'
    _description = "Operating Unit Mixin for Dependent Transactions"

    # Set through which field this model adopt another model's operating unit
    _ou_transaction = True

    def set_operating_unit_related(cls, follows_field):
        operating_unit_id = fields.Many2one(
            'operating.unit',
            string="Operating Unit",
            # we need to set this at class instanciation time,
            # but on inherited classes. Therefore this indirection.
            related=follows_field,
            store=True  # For reporting, speed
            # Defaults to readonly, which is intended.
        )
        setattr(cls, 'operating_unit_id', operating_unit_id)
