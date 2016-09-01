import os
class Model(Object):
    def __init__(self , collection):
        self.id = None
        dir_path = os.path.dirname(__file__)
        self.collection = os.path.join(dir_path , "../storage/"+collection+".json")

    def getById(self):
        pass

    def getAll(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    def toJson(self):
        pass

    def toModel(self):
        pass
