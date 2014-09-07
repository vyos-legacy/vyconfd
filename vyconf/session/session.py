class Session(object):
    def __init__(self,
                 running_config,
                 reference_tree,
                 user):
        self.__running_config = running_config
        self.__reference_tree = reference_tree
        self.__user = user
        self.level = None

    def configure(self):
        pass

    def set(self, path):
        pass

    def delete(self, path):
        pass

    def set_level(self, level):
        pass
        
    def commit(self):
        pass
