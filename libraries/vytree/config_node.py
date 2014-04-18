import vytree

class ConfigNode(vytree.Node):
    def __init__(self, name, parent=None):
        super(ConfigNode, self).__init__(name, parent)
        self.set_property("value_list", [])

    def add_value(self, value):
        self.get_property("value_list").append(value)

    def remove_value(self, value):
        self.get_property("value_list").remove(value)

    def get_values(self):
        return self.get_property("value_list")
