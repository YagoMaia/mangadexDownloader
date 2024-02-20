import redis
import json
from classes.singleton import Singleton

@Singleton
class Redis:
    def __init__(self):
        self.conection = redis.Redis(host="localhost", port=6379, decode_responses=True)
    
    def existsKey(self):
        return self.conection.exists("mangá")
    
    def setJson(self, value:dict):
        try:
            value_json = json.dumps(value)
            ret = self.conection.set("mangá", value_json)
            if ret:
                return True
        except Exception as error:
            return error
        
    def getJson(self):
        try:
            ret = self.conection.get("mangá")
            value_json = json.loads(ret)
            if ret:
                return value_json
        except Exception as error:
            return error