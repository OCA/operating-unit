# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from odoo import tools

class Container(object):
    pass

class ModelBuildingEvictor(object):
    """ Evict Odoo's model building in a given registry if the inherited model
    is not present in that registry. Cooperative pattern with the
    module-is-last-in-graph-ensurer, to make sure all potential candidate models
    are present in the registry. """

    # It's a python classmethod, not an odoo.api.model! That means it works on
    # ModelBuildingEvictor or it's python inherited class in a pre-odoo-model
    # state of the world.
    @classmethod
    def _build_model(cls, pool, cr):
        parents = cls._inherit
        parents = [parents] if isinstance(parents, tools.pycompat.string_types) else (parents or [])
        if any(model not in pool for model in parents):
            c = Container()
            # registry.descendants uses an OrderedSet. Yeah!
            # So we dummy assign one that's always there.
            c._name = 'ir.model'
            return c
        return super()._build_model(pool, cr)
