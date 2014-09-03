import os

from testtools import testcase

from vyconf.tree import referencetree as reftree


BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), )


DATA_DIR = os.environ.get(
    'VYCONF_DATA_DIR',
    os.path.join(BASE, '..', '..', 'data')
    )

TEST_DATA_DIR = os.environ.get(
    'VYCONF_TEST_DATA_DIR',
    os.path.join(BASE, 'data'))


class TestCase(testcase.TestCase):
    def get_loader(self, xml_file, types, schema_file):
        xml_path = os.path.join(TEST_DATA_DIR, xml_file)
        schema_path = os.path.join(DATA_DIR, schema_file)
        loader = reftree.ReferenceTreeLoader(
            xml_path, types, schema=schema_path)
        return loader
