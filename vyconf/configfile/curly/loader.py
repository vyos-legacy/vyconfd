#    vyconf.configfile.curly.loader: config loader that uses the AST
#        produced by curly parser
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

def load(ast, session, path=[]):
    for node in ast:
        value = node[1]
        name = value["name"]
        comment = value["comment"]

        if node[0] == "node":
            content = value["content"]
            new_path = path + name
            load(content, session, path=new_path)
        else:
            # This is a leaf node
            leaf_value = value["value"]
            final_path = path + name + [leaf_value]
            session.set(final_path)
        if comment:
            session.set_comment(path + name, comment)
    return None
