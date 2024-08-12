from json import JSONEncoder

from bson import json_util, ObjectId
from datetime import datetime
from decimal import Decimal

class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(obj, ObjectId):
            return str(obj)

        if isinstance(obj, Decimal):
            return float(obj)

        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)
