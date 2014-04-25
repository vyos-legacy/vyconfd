from lxml import etree as ET

import vytree

node_element = "node"
tag_node_element = "tagNode"
leaf_node_element = "leafNode"
name_constraint_element = "nameConstraint"


class ReferenceTreeLoader(object):
    def __init__(self, xml_source):
        self.__xml_tree = ET.parse(xml_source)
        self.__xml_root = self.__xml_tree.getroot()
        
    def load(self, reference_tree):
        self._walk_xml_node(self.__xml_root, reference_tree)

    def _add_reference_node(self, element):
        print "Adding element %s" % element.attrib["name"]

    def _walk_xml_leaf_node(self, node, reference_node):
        print "Adding leaf node %s" % node.tag

    def _walk_xml_node(self, xml_node, reference_node):
        for xml_child in xml_node:
            if (xml_child.tag == node_element) or (xml_child.tag == tag_node_element):
                next_reference_node = reference_node.insert_child([xml_child.attrib["name"]])
                self._walk_xml_node(xml_child, next_reference_node)
            elif xml_child.tag == name_constraint_element:
                #reference_node.set_name_constraint({"type": element.attrib["type"], "constraint": element.attrib["constraint"]})
                pass
            elif xml_child.tag == leaf_node_element:
                next_reference_node = reference_node.insert_child([xml_child.attrib["name"]])
                self._walk_xml_leaf_node(xml_child, next_reference_node)

