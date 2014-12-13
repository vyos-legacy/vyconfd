#!/usr/bin/env python
#
#    curly_parser_test.py:  tests for vyconf.configfile.curly.loader
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
import vyconf.configfile.curly as vcurly

TEST_CONFIG = """
foo {
  bar {
    baz 90 {
      /* Eggs */
      eggs "bazbaz";
    }
  }
  /* Quux */
  quux {
    /* Eggs eggs */
    eggs "eggs";
    spam "quuux";
    spam "quuuux";
  }
}
"""

DATA_DIR = os.environ.get(
    'VYCONF_DATA_DIR',
    os.path.join(os.getcwd(), 'data'))

TEST_DATA_DIR = os.environ.get(
    'VYCONF_TEST_DATA_DIR',
    os.path.join(os.path.join(os.getcwd(), 'vyconf/tests/integration/data')))

xml_0 = "session_test_0.xml"
xml_1 = "session_test_1.xml"
xml_path_0 = os.path.join(TEST_DATA_DIR, xml_0)
xml_path_1 = os.path.join(TEST_DATA_DIR, xml_1)
xmls = [xml_path_0, xml_path_1]
schema_file = "schemas/interface_definition.rng"

schema_path = os.path.join(DATA_DIR, schema_file)


class TestCurlyLoader(unittest.TestCase):
    def setUp(self):
        self.parser = vcurly.Parser()
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

        ast = self.parser.parse(TEST_CONFIG)
        vcurly.load(ast, self.session)

    def test_load_top_levels(self):
        self.assertTrue(self.session.exists(['foo']))
        self.assertTrue(self.session.exists(['foo', 'bar']))
        self.assertTrue(self.session.exists(['foo', 'quux']))

    def test_leaf_single_value(self):
        self.assertTrue(self.session.exists(
            ['foo', 'quux', 'eggs']))
        self.assertEqual(
            self.session.get_values(['foo', 'quux', 'eggs']),
            ['eggs'])

    def test_tag_node(self):
        # XXX: "foo bar baz 90" doesn't work
        self.assertTrue(self.session.exists(
            ['foo', 'bar', 'baz', 90, 'eggs', 'bazbaz']))

    def test_leaf_node_multiple_values(self):
        self.assertTrue(self.session.exists(
            ['foo', 'quux', 'spam', 'quuux']))
        self.assertTrue(self.session.exists(
            ['foo', 'quux', 'spam', 'quuuux']))

    def test_comment_leaf_node(self):
        self.assertEqual(
            self.session.get_comment(['foo', 'quux', 'eggs']),
            "Eggs eggs")

    def test_comment_nonleaf(self):
        self.assertEqual(
            self.session.get_comment(['foo', 'quux']),
            "Quux")
