#!/usr/bin/env python
#
#    test_session.py: integration tests for the session class
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

import os
import unittest

import vyconf.tree.configtree as vct
import vyconf.tree.referencetree as vrt
import vyconf.types as vtypes
import vyconf.types.dummy as dummytypes
import vyconf.session as vsession

DATA_DIR = os.environ.get(
    'VYCONF_DATA_DIR',
    os.path.join(os.getcwd(), 'data'))

TEST_DATA_DIR = os.environ.get(
    'VYCONF_TEST_DATA_DIR',
    os.path.join(os.path.join(os.getcwd(), 'tests/integration/data')))

xml_0 = "session_test_0.xml"
xml_1 = "session_test_1.xml"
xml_path_0 = os.path.join(TEST_DATA_DIR, xml_0)
xml_path_1 = os.path.join(TEST_DATA_DIR, xml_1)
xmls = [xml_path_0, xml_path_1]
schema_file = "schemas/interface_definition.rng"

schema_path = os.path.join(DATA_DIR, schema_file)


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.user = "vyconfadmin"
        self.types_dict = vtypes.get_types(dummytypes)
        self.rt = vrt.load_reference_tree(
            self.types_dict,
            xmls,
            schema_path)

        self.config_tree = vct.ConfigNode("root")
        self.validator = vrt.PathValidator(tree=self.rt, types=self.types_dict)
        self.session = vsession.Session(
            self.config_tree,
            self.validator,
            self.user)
        self.session.configure()

    def test_set(self):
        self.session.set(['foo', 'bar'])
        self.assertTrue(self.session.exists(['foo', 'bar']))

    def test_set_with_value(self):
        self.session.set(['foo', 'quux', 'spam', 'fgsfds'])
        self.assertTrue(self.session.exists(['foo', 'quux', 'spam', 'fgsfds']))

    def test_set_tag_node(self):
        self.session.set(
            ['foo', 'bar', 'baz', 'asdf', 'eggs', 'fghj'])
        self.assertTrue(
            self.session.exists(['foo', 'bar', 'baz', 'asdf', 'eggs', 'fghj']))
