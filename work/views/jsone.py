import json

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return [row for row in obj] 
