import os , json
class Model(object):
    def __init__(self , collection):
        self.id = None
        dir_path = os.path.dirname(__file__)
        self.collection = os.path.join(dir_path, "..", "storage", collection+".json")

    def get(self):
        return json.load(open(self.collection, "r"))

    def toJson(self, dict):
        open(self.collection, "w").write(json.dumps(dict))
