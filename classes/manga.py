from requests import Session
import utils.config as config
from classes.capitulos import Capitulos
from classes.cover import Cover
from utils import formatação_texto
from classes.singleton import Singleton

languages = ["pt-br"]

metodo_capitulos = Capitulos()
metodo_cover = Cover()


@Singleton
class Manga:
    """
    Classe responsável pelos métodos de baixar mangás
    """

    def __init__(self):
        self.session_manga = Session()

    def listar_mangas(self, nome_manga: str) -> dict | None:
        """
        Função responsável por listar os mangás que contenham o nome passado.

        Parâmetros:
            nome_manga : str -> Nome do mangá
        """
        print("\n   Iniciando conexão com MangaDex\n")
        r = self.session_manga.get(f"{config.BASE_URL}/manga", params={"title": nome_manga})
        mangas_achados = [manga for manga in r.json()["data"]]
        if len(mangas_achados) != 0:
            for index, m in enumerate(mangas_achados):
                title = m["attributes"]["title"]["en"]
                print(f"   [{index + 1}] - {title}")
            resp = input("\n   Qual mangá deseja selecionar? ")
            if resp == "nenhum":
                return None
            return mangas_achados[int(resp) - 1]
        return None

    def pegar_dados_manga(self, id_manga: str) -> dict:
        """
        Função responsável por pegar os dados do mangá.

        Parâmetros:
            id_manga : str -> Id do mangá
        """
        r = self.session_manga.get(f"{config.BASE_URL}/manga/{id_manga}")
        return r.json()

    def baixar_manga(self, nome_manga: str) -> None:
        """
        Função responsável por baixar os covers e os capitulos do mangá.

        Parâmetros:
            nome_manga: str -> Nome do mangá
        """
        manga_selecionado = self.listar_mangas(nome_manga)
        if manga_selecionado is not None:
            manga_id = manga_selecionado["id"]
            nome_manga = manga_selecionado["attributes"]["title"]["en"]

            lista_capitulos = metodo_capitulos.listar_capitulos(manga_id, "asc")
            listar_covers = metodo_cover.listar_covers(manga_id)

            capitulos = []

            for cap in lista_capitulos:
                id_capitulo = cap["id"]
                volume_capitulo = cap["attributes"]["volume"]
                n_capitulo = cap["attributes"]["chapter"]
                titulo_capitulo = cap["attributes"]["title"]
                capitulos.append(
                    {
                        "Num_Capitulo": n_capitulo,
                        "Id": id_capitulo,
                        "Titulo": titulo_capitulo,
                        "Volume": volume_capitulo,
                    }
                )

            capitulos_listados = metodo_capitulos.remover_capitulos_repetidos(capitulos)

            for index, cap_vol in enumerate(capitulos_listados):
                if (
                    index == 0
                    or capitulos_listados[index]["Volume"]
                    != capitulos_listados[index - 1]["Volume"]
                ):
                    volume = (cap_vol["Volume"] if cap_vol["Volume"] is not None else "Nenhum")
                    print(f"=========================== Volume {volume} ===========================")
                print(f"   ({index + 1}) - Capitulo {cap_vol['Num_Capitulo']} - {cap_vol['Titulo']}")

            # * Ajustar para poder escolher os capitulos para baixar

            print(f"\n   {len(capitulos_listados)} Capitulos encontrados\n")

            escolha_cap = input("   Quais capitulos deseja baixar? ")
            print("\n")

            if "-" in escolha_cap:
                cap_ini, cap_fim = escolha_cap.split("-")
                metodo_capitulos.baixar_capitulos( capitulos_listados, listar_covers, manga_id, nome_manga, int(cap_ini) - 1, int(cap_fim) - 1)
            elif "volume" in escolha_cap:
                volumes_escolhidos = escolha_cap.split()[1]
                for volume in volumes_escolhidos.split(","):
                    capitulos_volume = [cap for cap in capitulos_listados if cap["Volume"] == volume]
                    metodo_capitulos.baixar_capitulos( capitulos_volume, listar_covers, manga_id, nome_manga, 0, len(capitulos_volume) - 1)
            elif escolha_cap.isnumeric():
                metodo_capitulos.baixar_capitulos( capitulos_listados, listar_covers, manga_id, nome_manga, int(escolha_cap) - 1, int(escolha_cap) - 1)
            elif escolha_cap == "todos":
                metodo_capitulos.baixar_capitulos( capitulos_listados, listar_covers, manga_id, nome_manga, 0, len(capitulos_listados) - 1)
            elif escolha_cap == "nenhum":
                print("   Nenhum capitulo será baixado")
            else:
                print("   Opção não existente")
        else:
            print("   Mangá não encontrado")

    def status_manga(self, nome_manga: str) -> None:
        """
        Função responsável por retornar os status do mangá passado.

        Parâmetros:
            nome_manga : str -> Nome do mangá
        """
        manga_selecionado = self.listar_mangas(nome_manga)
        if manga_selecionado is not None:
            nome_manga = manga_selecionado["attributes"]["title"]["en"]
            descricao = manga_selecionado["attributes"]["description"]["pt-br"]
            ano_manga = manga_selecionado["attributes"]["year"]
            status = manga_selecionado["attributes"]["status"]
            formatação_texto.generate_ascii_art(nome_manga)
            print(f"Status: {status}")
            print(f"Ano Publicação: {ano_manga}")
            print(f"Descrição: {descricao}")
