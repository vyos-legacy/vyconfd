from lxml import etree as ET

import vytree

NODE_ELEMENT = "node"
TAG_NODE_ELEMENT = "tagNode"
LEAF_NODE_ELEMENT = "leafNode"
NAME_CONSTRAINT_ELEMENT = "nameConstraint"
VALUE_CONSTRAINT_ELEMENT = "valueConstraint"
HELP_STRING_ELEMENT = "helpString"
VALUE_HELP_STRING_ELEMENT = "valueHelpString"

NODE_NAME_ATTRIBUTE = "name"
TYPE_ATTRIBUTE = "type"
CONSTRAINT_ATTRIBUTE = "constraint"
DESCRIPTION_ATTRIBUTE = "description"

class ReferenceTreeLoader(object):
    def __init__(self, xml_source):
        self.__xml_tree = ET.parse(xml_source)
        self.__xml_root = self.__xml_tree.getroot()
        
    def load(self, reference_tree):
        self._walk_xml_node(self.__xml_root, reference_tree)

    def _walk_xml_leaf_node(self, node, reference_node):
        print "Adding leaf node %s" % node.tag

    def _walk_xml_node(self, xml_node, reference_node):
        for xml_child in xml_node:
            # <tagNode> can not contain another <tagNode>, but we do not reflect it here
            # because it's already expressed in the RELAX-NG XML grammar
            if (xml_child.tag == NODE_ELEMENT) or (xml_child.tag == TAG_NODE_ELEMENT):
                next_reference_node = reference_node.insert_child([xml_child.attrib[NODE_NAME_ATTRIBUTE]])
                self._walk_xml_node(xml_child, next_reference_node)
            elif xml_child.tag == NAME_CONSTRAINT_ELEMENT:
                # Blind faith here again, type= attribute is required by the grammar
                name_type = xml_child.attrib[TYPE_ATTRIBUTE]

                # constraint= arribute is optional, needs a check
                name_constraint = None
                if CONSTRAINT_ATTRIBUTE in xml_child.attrib:
                    name_constraint = xml_child.attrib[CONSTRAINT_ATTRIBUTE]

                reference_node.set_name_constraint(name_type, name_constraint)
            elif xml_child.tag == HELP_STRING_ELEMENT:
                help_string = xml_child.attrib[DESCRIPTION_ATTRIBUTE]
                reference_node.set_help_string(help_string)
            elif xml_child.tag == LEAF_NODE_ELEMENT:
                next_reference_node = reference_node.insert_child([xml_child.attrib[NODE_NAME_ATTRIBUTE]])
                self._walk_xml_leaf_node(xml_child, next_reference_node)

