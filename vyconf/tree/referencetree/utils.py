#    vyconf.tree.referencetree.utils:
#        auxillary functions for the reference tree.
#
#    Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA

from vyconf.tree.reference_node import ReferenceNode
from vyconf.tree.reference_tree_loader import ReferenceTreeLoader


def load_reference_tree(types, xml_sources, schema_source, tree=None):
    rt = None
    if not tree:
        rt = ReferenceNode("root")
    else:
        rt = tree

    if not isinstance(xml_sources, list):
        xml_sources = [xml_sources]

    for xml_source in xml_sources:
        rtl = ReferenceTreeLoader(xml_source, types, schema=schema_source)
        rtl.load(rt)

    return rt
