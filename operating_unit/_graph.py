# Copyright 2019 XOE Corp. SAS (XOE Solutions)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

"""
Ensure that this module is loaded last in the model graph. This ensures when
trying to overload the mixins, all inherited models will be already present.
"""


import odoo
from odoo import tools
from odoo.modules.module import load_information_from_description_file

TO_STACK_LAST = 'operating_unit'

def _clean_tree_from(module_list, module):
    """ Take out the module tree which is to be stacked last.
    module tree = module and it's dependent modules. """
    if module not in module_list:
        return module_list, []

    removed_tree = [module]
    module_list.remove(module)
    for remaining_module in module_list.copy():
        info = load_information_from_description_file(remaining_module)
        if any(dep for deb in info['depends'] if dep == module):
            removed_tree.append(remaining_module)
            module_list.remove(remaining_module)

    return module_list, removed_tree

def _add_depends_on_all(self, cr, modules, force):
    """ Alter (hack on) dependencies on the root module of the extracted module
    tree. Pipe rest of modules through the normal graph adding mechanics. """
    module = modules.pop(0)
    info = load_information_from_description_file(module)
    # Hack: make the first in row depend on all previously loaded
    # modules already in the graph (=self, a dict object)
    info['depends'] = set(self.keys())
    node = self.add_node(module, info)
    self.add
    for kind in ('init', 'demo', 'update'):
        if module in tools.config[kind] or 'all' in tools.config[kind] or kind in force:
            setattr(node, kind, True)
    # Just pipe the rest of the modules through normal add_modules call
    # Note: Calls again on the database diven package update
    # (self.update_from_db) updating ALL packages in the graph.
    self.add_modules(cr, modules, force=force)


class Graph(odoo.modules.graph.Graph):

    def add_modules(self, cr, module_list, force=None):
        module_list, removed_tree = _clean_tree_from(module_list, TO_STACK_LAST)
        res = super().add_modules(cr, module_list, force=force)
        if not removed_tree:
            return res
        _add_depends_on_all(self, cr, removed_tree, force)
        return res + len(removed_tree)

# Yeah, need to monkey patch
odoo.modules.graph.Graph = Graph
