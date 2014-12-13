#    vyconf.configfile.curly.renderer: curly config rendering functions
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


# XXX: make it a stream instead of doing rampant in-place
# string concatenation?

class Renderer(object):
    def __init__(self):
        self.tab_width = 4

    def _render_leaf_node(self, node, indent):
        name = node.get_name()
        values = node.get_values()
        node_str_list = map(lambda x: indent + name + " " + str(x) + ";", values)
        node_str = "\n".join(node_str_list)
        return node_str

    def _render_comment(self, node, indent):
        comment = node.get_comment()
        str = ""
        if comment:
            str = "\n" + indent + "/* " + comment + " */"
        return str

    def render(self, node, refnode, level=0):
        config = ""
        indent = " " * (self.tab_width * level)
        if node.is_empty() and refnode.is_leaf():
            config = config + self._render_comment(node, indent)
            config = config + "\n" + self._render_leaf_node(node, indent)
            return config

        for (child, rchild) in zip(node.get_children(), refnode.get_children()):
            if rchild.is_leaf():
                config = config + self._render_comment(child, indent)
                config = config + "\n" + self._render_leaf_node(child, indent)
            elif rchild.is_tag():
                name = child.get_name()
                tags = child.get_children()
                for tag in tags:
                    config = config + self._render_comment(tag, indent)
                    config = config + "\n" + indent + name + " " + str(tag.get_name()) + " {"
                    for (tag_child, tag_rchild) in zip(tag.get_children(), rchild.get_children()):
                        config = config +  self.render(tag_child, tag_rchild, level=level+1)
                    config = config + "\n" + indent + "}"
            else:
                name = child.get_name()
                comment = child.get_comment()
                config = config + self._render_comment(child, indent)
                config = config + "\n" + indent + str(name) + " {" + self.render(child, rchild, level=level+1) + "\n" + indent + "}"

        return config
