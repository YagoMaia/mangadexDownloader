import json
import os
import utils.config as config
from classes.manga import Manga
from classes.capitulos import Capitulos
from classes.redis import Redis
# * Mangas no Json Mangas Diários

metodos_mangas = Manga()
metodo_capitulos = Capitulos()
metodos_redis = Redis()
class MangasDiarios:

    # def atualizar_json(self, mangas_json: dict) -> None:
    #     """
    #     Função responsável por 
    #     """
    #     with open(f"{config.PATH_JSON}/mangas_diarios.json", "w") as ponteiro_json:
    #         json.dump(mangas_json, ponteiro_json)

    def json_mangas_diarios(self) -> None:
        """
        Função responsável por retornar o Json que está no Redis com os mangás atuais.
        """
        if metodos_redis.existsKey():
            return metodos_redis.getJson()
        metodos_redis.setJson({"Atuais":[]})
        return metodos_redis.getJson()

    def atualizar_leituras(self) -> None:
        """
        Função responsável por atualizar as leituras no redis.
        """
        mangas_atuais = self.json_mangas_diarios()
        for manga in mangas_atuais['Atuais']:
            print(f"\n   Verificando Mangá: {manga['Titulo']}")
            dados_ultimo_cap = metodo_capitulos.listar_ultimo_capitulo(manga['Id'])
            ultima_cap_add = dados_ultimo_cap['attributes']['chapter']
            if ultima_cap_add != manga['Ultimo_Cap']:
                print("   Capitulo novo a ser lido")
                novo_cap_a_ser_lido = metodo_capitulos.listar_ultimo_capitulo(manga['Id'])
                n_capitulo = novo_cap_a_ser_lido['attributes']["chapter"]
                titulo_capitulo = novo_cap_a_ser_lido['attributes']['title']
                print(f"   Capitulo: {n_capitulo} - {titulo_capitulo}")
                print(f"   Cod Antigo: {manga['Ultimo_Cap']} - Cod Novo: {ultima_cap_add}")
                manga['Ultimo_Cap'] = ultima_cap_add
            else:
                print("   Nenhum capitulo novo adicionado")
        metodos_redis.setJson(mangas_atuais)

    def adicionar_manga_diario(self, nome_manga:str) -> None:
        """
        Função responsável por adicoinar um novo mangá na lista de mangaś atuais.
        
        Parâmetros:
            nome_manga : str -> Nome do mangá
        """
        manga_selecionado = metodos_mangas.listar_mangas(nome_manga)
        if manga_selecionado is not None:
            manga_id = manga_selecionado['id']
            nome_manga = manga_selecionado["attributes"]['title']['en']
            dados_ultima_cap_add = metodo_capitulos.listar_ultimo_capitulo(manga_id)
            ultimo_cap = dados_ultima_cap_add['attributes']['chapter']
            novo_manga = {'Titulo': nome_manga,'Id': manga_id, 'Ultimo_Cap': ultimo_cap}
            repetido = False

            mangas_atuais = self.json_mangas_diarios()
            for m in mangas_atuais['Atuais']:
                if m['Titulo'] == novo_manga['Titulo']:
                    repetido = True
            if repetido == False:
                mangas_atuais['Atuais'].append(novo_manga)
                metodos_redis.setJson(mangas_atuais)
                print(
                    f"\n   {novo_manga['Titulo']} adicionado na lista de mangás Atuais")
            else:
                print("\n   Mangá repetido")

    def remover_manga_diario(self, indice: int) -> None:
        """
        Função responsável por remover um mangá da lista de mangaś atuais.
        
        Parâmetros:
            indice: int -> Índice do mangá que será deletado
        """
        mangas_atuais = self.json_mangas_diarios()
        mangas_atuais['Atuais'].pop(indice)
        metodos_redis.setJson(mangas_atuais)
        print("\n   Mangá removido")

    def listar_mangas_diarios(self) -> None:
        """
        Função responsável por listar os mangás atuais.
        """
        mangas_atuais = self.json_mangas_diarios()
        print("\n   Mangas na lista de atuais\n")
        for index, m in enumerate(mangas_atuais['Atuais']):
            print(f"   {index+1} - {m['Titulo']}")
