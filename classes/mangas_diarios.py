import json
import os
import config
from classes.manga import Manga
# * Mangas no Json Mangas Diários

metodos_mangas = Manga()

class MangasDiarios:

    def atualizar_json(self, mangas_json):
        with open(f"{config.PATH_JSON}/mangas_diarios.json", "w") as ponteiro_json:
            json.dump(mangas_json, ponteiro_json)

    def json_mangas_diarios(self):
        if os.path.exists(f"{config.PATH_JSON}/mangas_diarios.json"):
            with open(f"{config.PATH_JSON}/mangas_diarios.json", "r") as mangas_diarios:
                data = json.load(mangas_diarios)
        else:
            data = {"Atuais": []}
            with open(f"{config.PATH_JSON}/mangas_diarios.json", "w+") as mangas_diarios:
                json.dump(data, mangas_diarios)
        return data

    def atualizar_leituras(self):
        mangas_atuais = self.json_mangas_diarios()
        for manga in mangas_atuais['Atuais']:
            print(f"\n  Verificando Mangá: {manga['Titulo']}")
            dados = metodos_mangas.pegar_dados_manga(manga['Id'])
            ultima_cap_add = dados["data"]['attributes']['latestUploadedChapter']
            if ultima_cap_add != manga['Ultimo_Cap']:
                print("\n   Capitulo novo a ser lido")
                novo_cap_a_ser_lido = metodos_mangas.listar_ultimo_capitulo(manga['Id'])
                n_capitulo = novo_cap_a_ser_lido['attributes']["chapter"]
                titulo_capitulo = novo_cap_a_ser_lido['attributes']['title']
                print(f"    Capitulo: {n_capitulo} - {titulo_capitulo}")
                manga['Ultimo_Cap'] = ultima_cap_add
            else:
                print("\n   Nenhum capitulo novo adicionado")
        self.atualizar_json(mangas_atuais)

    def adicionar_manga_diario(self, nome_manga):

        manga_selecionado, mensagem = metodos_mangas.listar_mangas(nome_manga)
        if manga_selecionado is not None:
            manga_id = manga_selecionado['id']
            nome_manga = manga_selecionado["attributes"]['title']['en']
            ultima_cap_add = manga_selecionado['attributes']['latestUploadedChapter']
            novo_manga = {'Titulo': nome_manga,'Id': manga_id, 'Ultimo_Cap': ultima_cap_add}
            repetido = False

            mangas_atuais = self.json_mangas_diarios()
            for m in mangas_atuais['Atuais']:
                if m['Titulo'] == novo_manga['Titulo']:
                    repetido = True
            if repetido == False:
                mangas_atuais['Atuais'].append(novo_manga)
                with open(f"{config.PATH_JSON}/mangas_diarios.json", "w") as ponteiro_json:
                    json.dump(mangas_atuais, ponteiro_json)
                print(
                    f"\n    Mangá {novo_manga['Titulo']} adicionado na lista de mangás Atuais")
            else:
                print("\n    Mangá repetido")

    def remover_manga_diario(self, indice: int):

        mangas_atuais = self.json_mangas_diarios()
        mangas_atuais['Atuais'].pop(indice)
        with open(f"{config.PATH_JSON}/mangas_diarios.json", "w") as ponteiro_json:
            json.dump(mangas_atuais, ponteiro_json)
        print("\n   Mangá removido")

    def listar_mangas_diarios(self):

        mangas_atuais = self.json_mangas_diarios()
        print("\n   Mangas na lista de atuais\n")
        for index, m in enumerate(mangas_atuais['Atuais']):
            print(f"{index+1} - {m['Titulo']}")
