import redis
import json
from classes.singleton import Singleton


@Singleton
class Redis:
    def __init__(self):
        self.conection = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def existsKey(self):
        """
        Função responsável por verificar se existe essa chave no redis.
        """
        return self.conection.exists("mangá")

    def setJson(self, value: dict) -> bool:
        """
        Função responsável por setar o Json no redis, retornando um booleano.

        Parâmetros:
            value : dict -> Dicionário que será adicionado ao redis na chave mangá
        """
        try:
            value_json = json.dumps(value)
            ret = self.conection.set("mangá", value_json)
            if ret:
                return True
            return False
        except Exception:
            return False

    def getJson(self) -> dict | Exception:
        """
        Função responsável por pegar o Json no redis.
        """
        try:
            ret = self.conection.get("mangá")
            value_json = json.loads(ret)
            if ret:
                return value_json
            return {}
        except Exception as error:
            return error
