import requests
import config
import os
import alive_progress 
from classes.cover import Cover

metodo_cover = Cover()

languages =['pt-br']


class Capitulos:
    def remover_capitulos_repetidos(self, capitulos:list):
        capitulos_vistos = set()
        capitulos_para_remover = []

        for i, manga in enumerate(capitulos):
            cap = manga['Num_Capitulo']
            if cap in capitulos_vistos:
                capitulos_para_remover.append(i)
            else:
                capitulos_vistos.add(cap)

        for indice in reversed(capitulos_para_remover):
            del capitulos[indice]
        
        return capitulos

    def buscar_dados_capitulo(self, id_capitulo):
        chap = requests.get(f"{config.BASE_URL}/at-home/server/{id_capitulo}")
        return chap.json()

    def listar_capitulos(self, manga_id):
        r1 = requests.get(f"{config.BASE_URL}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages, 'limit':500})
        if r1.json()['total'] > 500:
            print("    Mais de 500 capitulos encontrados")
        #r2 = requests.get(f"{config.BASE_URL}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages, 'limit': limit, 'order[chapter]':'asc'})
        return r1.json()['data']
    
    def listar_ultimo_capitulo(self, manga_id):
        r2 = requests.get(f"{config.BASE_URL}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages, 'limit': 1, 'order[chapter]':'desc'})
        return r2.json()['data'][0]
    
    def organizar_capitulos(self, lista_capitulos):
        capitulos_sem_repeticao = self.remover_capitulos_repetidos(lista_capitulos)
        return capitulos_sem_repeticao
    
    def baixar_capitulos(self, capitulos, covers, manga_id, nome_manga, inicio, fim):
        
        for i in range(inicio, fim + 1):
            chap_id = capitulos[i]['Id']
            num_chap = capitulos[i]['Num_Capitulo']
            vol_chap = capitulos[i]['Volume']
            
            if vol_chap == None:
                vol_chap = "Nenhum"
            
            chap = self.buscar_dados_capitulo(chap_id)

            folder_path = f"/mnt/76C08D67C08D2E85/Mangás/{nome_manga}/Volume {vol_chap}/Capitulo {num_chap}"
            os.makedirs(folder_path, exist_ok=True)
            
            host = chap["baseUrl"]
            chapter_hash = chap["chapter"]["hash"]
            data_saver = chap["chapter"]["dataSaver"]
            data = chap["chapter"]["data"]
            
            metodo_cover.baixar_cover(covers, vol_chap, manga_id, nome_manga)
            
            with alive_progress.alive_bar(len(data_saver), title = f"Capitulo {num_chap} - Vol {vol_chap}") as bar:
                for index, page in enumerate(data_saver):
                    if not os.path.exists(f"{folder_path}/Page {index}"):
                        r = requests.get(f"{host}/data-saver/{chapter_hash}/{page}")
                        if r.status_code == 404:
                            page = data[index]
                            r = requests.get(f"{host}/data/{chapter_hash}/{page}")
                        with open(f"{folder_path}/Page {index}", mode="wb") as f:
                            f.write(r.content)
                    bar()