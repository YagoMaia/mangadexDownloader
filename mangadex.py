import sys
from classes.manga import Manga
from classes.mangas_diarios import MangasDiarios
from utils.formatação_texto import generate_ascii_art

title = sys.argv[1]

leituras_atuais = MangasDiarios()
download_manga = Manga()

print(generate_ascii_art("MangaDex"))

match title:
    case "diario":
        leituras_atuais.atualizar_leituras()
    
    case "adicionar":
        nome_manga = sys.argv[2]
        lista_mangas = nome_manga.split(",")
        for manga in lista_mangas:
            leituras_atuais.adicionar_manga_diario(manga.strip())
    
    case "remover":
        numero_manga = int(sys.argv[2])
        leituras_atuais.remover_manga_diario(numero_manga - 1)
        
    case "listar":
        leituras_atuais.listar_mangas_diarios()
    
    case "status":
        nome_manga = sys.argv[2]
        download_manga.status_manga(nome_manga)
    
    case _:
        download_manga.baixar_manga(title)

