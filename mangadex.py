import sys
from utils.dados_mangas import DadosMangas
from utils.mangas_diarios import MangasDiarios

title = sys.argv[1]

leituras_atuais = MangasDiarios()
download_manga = DadosMangas()

match title:
    case "diario":
        leituras_atuais.atualizar_leituras()
    
    case "adicionar":
        nome_manga = sys.argv[2]
        leituras_atuais.adicionar_manga_diario(nome_manga)
    
    case "remover":
        numero_manga = int(sys.argv[2])
        leituras_atuais.remover_manga_diario(numero_manga - 1)
        
    case "listar":
        leituras_atuais.listar_mangas_diarios()
    
    case _:
        download_manga.baixar_manga(title)

