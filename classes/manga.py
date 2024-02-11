import requests
import config
from classes.capitulos import Capitulos
from classes.cover import Cover
from utils import formatação_texto

languages =['pt-br']

metodo_capitulos = Capitulos()
metodo_cover = Cover()

class Manga:
    def listar_mangas(self, titulo_manga):
        print("\n    Iniciando conexão com MangaDex\n")
        r = requests.get(f"{config.BASE_URL}/manga", params={"title": titulo_manga})
        mangas_achados = [manga for manga in r.json()["data"]]
        if len(mangas_achados) != 0:
            for index, m in enumerate(mangas_achados):
                title = m["attributes"]['title']['en']
                print(f"[{index + 1}] - {title}")
            resp = int(input("\n    Qual mangá deseja selecionar? ")) - 1
            return mangas_achados[resp]
        return None

    def pegar_dados_manga(self, id_manga):
        r = requests.get(f"{config.BASE_URL}/manga/{id_manga}")
        return r.json()        
    
    def baixar_manga(self, nome_manga):
        manga_selecionado = self.listar_mangas(nome_manga)
        if manga_selecionado is not None:
        
            manga_id = manga_selecionado['id']
            nome_manga = manga_selecionado["attributes"]['title']['en'] 

            lista_capitulos = metodo_capitulos.listar_capitulos(manga_id)
            listar_covers = metodo_cover.listar_covers(manga_id)
            
            capitulos = []

            for cap in lista_capitulos:
                id_capitulo = cap["id"]
                volume_capitulo = cap['attributes']["volume"]
                n_capitulo = cap['attributes']["chapter"]
                titulo_capitulo = cap['attributes']['title']
                capitulos.append({'Num_Capitulo': n_capitulo, 'Id':id_capitulo, 'Titulo': titulo_capitulo, 'Volume':volume_capitulo})

            capitulos_listados = metodo_capitulos.organizar_capitulos(capitulos)

            for index, cap_vol in enumerate(capitulos_listados):
                print(f"({index + 1}) - Capitulo {cap_vol['Num_Capitulo']} - {cap_vol['Titulo']}")

            #* Ajustar para poder escolher os capitulos para baixar

            print(f"    \n{len(capitulos_listados)} Capitulos encontrados\n")

            escolha_cap = input("Quais capitulos deseja baixar? ")
            print("\n")
            
            if "-" in escolha_cap:
                cap_ini, cap_fim = escolha_cap.split("-")
                metodo_capitulos.baixar_capitulos(capitulos_listados, listar_covers, manga_id, nome_manga, int(cap_ini) - 1, int(cap_fim) - 1)
            elif escolha_cap.isnumeric():
                metodo_capitulos.baixar_capitulos(capitulos_listados, listar_covers, manga_id, nome_manga, int(escolha_cap) - 1, int(escolha_cap) - 1)
            elif escolha_cap == "todos":
                metodo_capitulos.baixar_capitulos(capitulos_listados, listar_covers, manga_id, nome_manga, 0, len(capitulos_listados) - 1)
            elif escolha_cap == "nenhum":
                print("    Nenhum capitulo será baixado")
            else:
                print("    Opção não existente")
        else:
            print("    Mangá não encontrado")
            
    def status_manga(self, nome_manga):
        manga_selecionado = self.listar_mangas(nome_manga)
        if manga_selecionado is not None:
            nome_manga = manga_selecionado["attributes"]['title']['en'] 
            descricao = manga_selecionado["attributes"]['description']['pt-br'] 
            ano_manga = manga_selecionado["attributes"]['year']
            status = manga_selecionado["attributes"]['status']
            print(formatação_texto.generate_ascii_art(nome_manga))
            print(f"Status: {status}")
            print(f"Ano Publicação: {ano_manga}")
            print(f"Descrição: {descricao}")