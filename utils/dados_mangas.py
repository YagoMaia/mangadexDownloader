import requests
import config
import os
import alive_progress 

languages =['pt-br']

#* Funções para baixar capitulos e mostrar mangás disponíveis

class DadosMangas:
    def remover_repetidos(self, capitulos:list):
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
        r1 = requests.get(f"{config.BASE_URL}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages})
        limit = r1.json()['total'] if r1.json()['total'] <= 500 else 500
        r2 = requests.get(f"{config.BASE_URL}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages, 'limit': limit, 'order[chapter]':'asc'})
        return r2.json()['data']
    
    def listar_ultimo_capitulo(self, manga_id):
        r2 = requests.get(f"{config.BASE_URL}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages, 'limit': 1, 'order[chapter]':'desc'})
        return r2.json()['data'][0]
    
    def organizar_capitulos(self, lista_capitulos):
        #capitulos_organizados = sorted(lista_capitulos, key=lambda x : float(x['Num_Capitulo']))
        capitulos_sem_repeticao = self.remover_repetidos(lista_capitulos)
        return capitulos_sem_repeticao

    def baixar_capitulos(self, capitulos, nome_manga, inicio, fim):
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
                #print("Cápitulo já existente")

    def listar_mangas(self, titulo_manga):
        print("\n    Iniciando conexão com MangaDex\n")
        r = requests.get(f"{config.BASE_URL}/manga", params={"title": titulo_manga})
        mangas_achados = [manga for manga in r.json()["data"]]
        if len(mangas_achados) != 0:
            for index, m in enumerate(mangas_achados):
                title = m["attributes"]['title']['en']
                print(f"    [{index + 1}] - {title}")
            resp = int(input("\n    Qual mangá deseja selecionar? ")) - 1
            titulo_manga_selecionado = mangas_achados[resp]['attributes']['title']['en']
            return mangas_achados[resp], f"\n    {titulo_manga_selecionado} selecionado"
        return None, "\n    Mangá não encontrado"

    def pegar_dados_manga(self, id_manga):
        r = requests.get(f"{config.BASE_URL}/manga/{id_manga}")
        return r.json()

    def baixar_manga(self, nome_manga):
        manga_selecionado, mensagem = self.listar_mangas(nome_manga)
        print(mensagem)
        if manga_selecionado is not None:
        
            manga_id = manga_selecionado['id']
            nome_manga = manga_selecionado["attributes"]['title']['en'] 

            lista_capitulos = self.listar_capitulos(manga_id)
            
            capitulos = []

            for cap in lista_capitulos:
                id_capitulo = cap["id"]
                volume_capitulo = cap['attributes']["volume"]
                n_capitulo = cap['attributes']["chapter"]
                titulo_capitulo = cap['attributes']['title']
                capitulos.append({'Num_Capitulo': n_capitulo, 'Id':id_capitulo, 'Titulo': titulo_capitulo, 'Volume':volume_capitulo})

            capitulos_listados = self.organizar_capitulos(capitulos)
            #capitulos_listados = capitulos

            for index, cap_vol in enumerate(capitulos_listados):
                print(f"    ({index + 1}) - Capitulo {cap_vol['Num_Capitulo']} - {cap_vol['Titulo']}")

            #* Ajustar para poder escolher os capitulos para baixar

            print(f"\n    {len(capitulos_listados)} Capitulos encontrados\n")

            escolha_cap = input("    Quais capitulos deseja baixar? ")
            print("\n")
            
            if "-" in escolha_cap:
                cap_ini, cap_fim = escolha_cap.split("-")
                self.baixar_capitulos(capitulos_listados, nome_manga, int(cap_ini) - 1, int(cap_fim) - 1)
            elif escolha_cap.isnumeric():
                self.baixar_capitulos(capitulos_listados, nome_manga, int(escolha_cap) - 1, int(escolha_cap) - 1)
            elif escolha_cap == "todos":
                self.baixar_capitulos(capitulos_listados, nome_manga, 0, len(capitulos_listados))
            elif escolha_cap == "nenhum":
                print("    Nenhum capitulo será baixado")
            else:
                print("    Opção não existente")
        else:
            print("    Mangá não encontrado")