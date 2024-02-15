from requests import Session
import utils.config as config
import os
import alive_progress 
from classes.singleton import Singleton

languages =['pt-br']

@Singleton
class Cover:
    def __init__(self):
        self.session_cover = Session()
    
    def remover_covers_repetidos(self, covers:list):
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

    def baixar_cover(self, covers, volume, manga_id, nome_manga):
        if volume.isnumeric():
            folder_volume = f"/mnt/76C08D67C08D2E85/Mangás/{nome_manga}/Volume {volume}"
            
            cover_vol = covers[int(volume) - 1]
            cover_file = cover_vol['attributes']['fileName']
            
            if not os.path.exists(f"{folder_volume}/Capa Volume {volume}.png"):
                with alive_progress.alive_bar(1, title = f"Capa Volume {volume}") as bar:
                    r = self.session_cover.get(f"{config.PATH_COVER}/{manga_id}/{cover_file}")
                    with open(f"{folder_volume}/Capa Volume {volume}.png", mode="wb") as f:
                        f.write(r.content)
                    bar()
                    
    def listar_covers(self, id_manga):
        covers = self.session_cover.get(f"{config.BASE_URL}/cover", params = {"manga[]":id_manga, 'limit':100, 'order[volume]':'asc'})
        covers_sem_repeticao = self.remover_covers_repetidos(covers.json()['data'])
        return covers_sem_repeticao