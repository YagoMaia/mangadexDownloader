from requests import Session
import utils.config as config
import os
import alive_progress
from classes.cover import Cover
from classes.singleton import Singleton
from utils.notification import notification

metodo_cover = Cover()

languages = ["pt-br"]


@Singleton
class Capitulos:
    """
    Classe responsável pelos métodos de baixar capitulos
    """

    def __init__(self):
        self.session_capitulos = Session()

    def remover_capitulos_repetidos(self, capitulos: list) -> list:
        """
        Função responsável por remover os capitulos repetidos da lista.

        Parâmetros:
            capitulos: List -> lista dos capitulso
        """
        capitulos_vistos = set()
        capitulos_para_remover = []

        for i, manga in enumerate(capitulos):
            cap = manga["Num_Capitulo"]
            if cap in capitulos_vistos:
                capitulos_para_remover.append(i)
            else:
                capitulos_vistos.add(cap)

        for indice in reversed(capitulos_para_remover):
            del capitulos[indice]

        return capitulos

    def buscar_dados_capitulo(self, id_capitulo: str) -> dict:
        """
        Função responsável por retornar os dados do capitulos.

        Parâmetros:
            id_capitulo: str -> id do capitulo
        """
        chap = self.session_capitulos.get(f"{config.BASE_URL}/at-home/server/{id_capitulo}")
        return chap.json()

    def listar_capitulos(self, id_manga: str, order: str = "asc") -> dict:
        """
        Função responsável por retornar a lista de capitulos existentes do mangá.

        Parâmetros:
            id_manga: str -> id do mangá selecionado
        """
        r1 = self.session_capitulos.get(
            f"{config.BASE_URL}/manga/{id_manga}/feed",
            params={
                "translatedLanguage[]": languages,
                "limit": 500,
                "order[chapter]": order,
            },
        )
        total_cap = r1.json()["total"]
        capitulos = r1.json()["data"]
        cap_listados = 500
        while cap_listados < total_cap:
            r2 = self.session_capitulos.get(
                f"{config.BASE_URL}/manga/{id_manga}/feed",
                params={
                    "translatedLanguage[]": languages,
                    "limit": 500,
                    "offset": cap_listados,
                    "order[chapter]": order,
                },
            )
            capitulos.extend(r2.json()["data"])
            cap_listados += 500
        return capitulos

    def listar_ultimo_capitulo(self, id_manga: str) -> dict:
        """
        Função responsável por retornar os dados do ultimo capitulo publicado.

        Parâmetros:
            id_manga: str -> id do mangá selecionado
        """
        r2 = self.session_capitulos.get(
            f"{config.BASE_URL}/manga/{id_manga}/feed",
            params={
                "translatedLanguage[]": languages,
                "limit": 1,
                "order[chapter]": "desc",
            },
        )
        return r2.json()["data"][0]

    def baixar_capitulos( self, capitulos: list, covers: list, id_manga: str, nome_manga: str, inicio: int, fim: int) -> None:
        """
        Função responsável por baixar os capitulos.

        Parâmetros:
            capitulos: List -> lista dos capitulos
            covers: List -> lista dos covers
            id_manga: str -> id do mangá
            nome_manga: str -> Nome do mangá
            inicio : int -> Capitulo inicial
            fim: int -> Captitulo final
        """

        for i in range(inicio, fim + 1):
            chap_id = capitulos[i]["Id"]
            num_chap = capitulos[i]["Num_Capitulo"]
            vol_chap = capitulos[i]["Volume"]

            if vol_chap is None:
                vol_chap = "Nenhum"
            folder_path = f"{config.PATH_DOWNLOAD}/{nome_manga}/Volume {vol_chap}/Capitulo #{num_chap} - {nome_manga}"
            if vol_chap.isnumeric():
                folder_path = f"{config.PATH_DOWNLOAD}/{nome_manga}/Volume {int(vol_chap):03d}/Capitulo #{num_chap} - {nome_manga}"
            if not os.path.exists(folder_path):
                chap = self.buscar_dados_capitulo(chap_id)

                os.makedirs(folder_path, exist_ok=True)

                host = chap["baseUrl"]
                chapter_hash = chap["chapter"]["hash"]
                data_saver = chap["chapter"]["dataSaver"]
                data = chap["chapter"]["data"]

                metodo_cover.baixar_cover(covers, vol_chap, id_manga, nome_manga)

                with alive_progress.alive_bar(len(data_saver) - 1, title=f"Capitulo {num_chap} - Vol {vol_chap}") as bar:
                    for index, page in enumerate(data_saver):
                        if index in (0, len(data_saver)):
                            continue
                        if not os.path.exists(f"{folder_path}/Page {index:02d}.jpg"):
                            r = self.session_capitulos.get(f"{host}/data-saver/{chapter_hash}/{page}")
                            if r.status_code == 404:
                                page = data[index]
                                r = self.session_capitulos.get(f"{host}/data/{chapter_hash}/{page}")
                            with open(f"{folder_path}/Page {index:02d}.jpg", mode="wb") as f:
                                f.write(r.content)
                        bar()
        notification(nome_manga, "Capitulos Baixado com sucesso")
