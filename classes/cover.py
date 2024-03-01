from requests import Session
import utils.config as config
import os
import alive_progress 
from classes.singleton import Singleton

languages =['pt-br']

@Singleton
class Cover:
    """
    Classe responsável pelos métodos de baixar covers
    """
    
    def __init__(self):
        self.session_cover = Session()
    
    def remover_covers_repetidos(self, covers: list) -> list:
        """
        Função responsável por remover os covers antigos.
        
        Parâmetros:
            covers : list -> Lista de covers
        """
        covers_vistos = set()
        covers_para_remover = []

        for i, cover in enumerate(covers):
            cap = cover['attributes']['volume']
            if cap in covers_vistos:
                covers_para_remover.append(i)
            else:
                covers_vistos.add(cap)

        for indice in reversed(covers_para_remover):
            del covers[indice]
        
        return covers

    def baixar_cover(self, covers: list, volume: str, id_manga: str, nome_manga: str) -> None:
        """
        Função responsável por baixar o cover.
        
        Parâmetros:
            covers : list -> Lista de covers
            volume : str -> volume do capitulo
            id_manga : str -> Id do mangá
            nome_manga : str -> Nome do mangá
        """
        if volume.isnumeric():
            folder_volume = f"{config.PATH_DOWNLOAD}/{nome_manga}/Volume {int(volume):03d}"
            
            cover_vol = covers[int(volume) - 1]
            cover_file = cover_vol['attributes']['fileName']
            
            if not os.path.exists(f"{folder_volume}/Capa Volume {volume}.jpg"):
                with alive_progress.alive_bar(1, title = f"Capa Volume {volume}") as bar:
                    r = self.session_cover.get(f"{config.PATH_COVER}/{id_manga}/{cover_file}")
                    with open(f"{folder_volume}/Capa Volume {volume}.jpg", mode="wb") as f:
                        f.write(r.content)
                    bar()
                    
    def listar_covers(self, id_manga: str) -> list:
        """
        Função responsável por listar os covers do mangá.
        
        Parâmetros:
            id_manga: Id do mangá
        """
        covers = self.session_cover.get(f"{config.BASE_URL}/cover", params = {"manga[]":id_manga, 'limit':100, 'order[volume]':'asc'})
        covers_sem_repeticao = self.remover_covers_repetidos(covers.json()['data'])
        return covers_sem_repeticao