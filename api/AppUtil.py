import json
from bson import ObjectId
from pymongo.results import DeleteResult

class JSONEncoder(json.JSONEncoder):
    def __init__(self):
        pass
    def default(self, o):
        print(o)
        print(type(o))

        if(isinstance(o, ObjectId) or isinstance(o, DeleteResult)):
            return str(o)
        return json.JSONEncoder.default(self, o)


