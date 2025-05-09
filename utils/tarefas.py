from celery import Celery
from utils import config
import os
import requests


app = Celery('task', broker = "redis://localhost:6379/1")
app.conf.broker_connection_retry_on_startup = True


def buscar_dados_capitulo(id_capitulo: str) -> dict:
        """
        Função responsável por retornar os dados do capitulos.

        Parâmetros:
            id_capitulo: str -> id do capitulo
        """
        chap = requests.get(f"{config.BASE_URL}/at-home/server/{id_capitulo}")
        return chap.json()

@app.task(name = "baixar_cover")
def baixar_cover(covers: list, id_manga: str, nome_manga: str) -> bool:
    """
    Tarefa responsável por baixar o cover.

    Parâmetros:
        covers : list -> Lista de covers
        volume : str -> volume do capitulo
        id_manga : str -> Id do mangá
        nome_manga : str -> Nome do mangá
    """
    lista_retornos = []
    folder_manga = f"{config.PATH_DOWNLOAD}/{nome_manga}"
    for folder in os.listdir(folder_manga):
        volume = folder.split(" ")[1]
        if volume.isnumeric():
            volume = int(volume)
            print(volume)
            cover_vol = covers[volume - 1]
            cover_file = cover_vol["attributes"]["fileName"]
            folder_volume = f"{folder_manga}/{folder}"
            if not os.path.exists(f"{folder_volume}/Capa Volume {volume}.jpg"):
                r = requests.get(f"{config.PATH_COVER}/{id_manga}/{cover_file}")
                with open(f"{folder_volume}/Capa Volume {volume}.jpg", mode="wb") as f:
                    f.write(r.content)
                    lista_retornos.append(True)
            lista_retornos.append(False)
    return lista_retornos

@app.task(name = "baixar_capitulo")
def baixar_capitulos(capitulo: dict, nome_manga: str) -> bool:
    """
    Tarefa responsável por baixar os capitulos.

    Parâmetros:
        capitulos: List -> lista dos capitulos
        covers: List -> lista dos covers
        id_manga: str -> id do mangá
        nome_manga: str -> Nome do mangá
        inicio : int -> Capitulo inicial
        fim: int -> Captitulo final
    """

    chap_id = capitulo["Id"]
    num_chap = capitulo["Num_Capitulo"] if capitulo["Num_Capitulo"] is not None else 0
    vol_chap = capitulo["Volume"]

    if vol_chap is None:
        vol_chap = "Nenhum"
    folder_path = f"{config.PATH_DOWNLOAD}/{nome_manga}/Volume {vol_chap}/Capitulo #{num_chap} - {nome_manga}"
    if vol_chap.isnumeric():
        folder_path = f"{config.PATH_DOWNLOAD}/{nome_manga}/Volume {int(vol_chap):03d}/Capitulo #{num_chap} - {nome_manga}"
    if not os.path.exists(folder_path):
        chap = buscar_dados_capitulo(chap_id)

        os.makedirs(folder_path, exist_ok=True)

        host = chap["baseUrl"]
        chapter_hash = chap["chapter"]["hash"]
        data_saver = chap["chapter"]["dataSaver"]
        data = chap["chapter"]["data"]

        for index, page in enumerate(data_saver):
            if index in (0, len(data_saver)):
                continue
            if not os.path.exists(f"{folder_path}/Cap_{int(num_chap):04d}-Page {index:02d}.jpg"):
                r = requests.get(f"{host}/data-saver/{chapter_hash}/{page}")
                if r.status_code == 404:
                    page = data[index]
                    r = requests.get(f"{host}/data/{chapter_hash}/{page}")
                with open(f"{folder_path}/Cap_{int(num_chap):04d}-Page {index:02d}.jpg", mode="wb") as f:
                    f.write(r.content)
    #notification(nome_manga, "Capitulos Baixado com sucesso")
    return True