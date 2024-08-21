from classes.mangas_diarios import MangasDiarios
from utils.formatação_texto import generate_ascii_art
from utils.notification import notification

notification("Teste", "Teste")

generate_ascii_art("   MangaDex")
leituras_atuais = MangasDiarios()
print("Iniciando consulta mangás diarios")
leituras_atuais.atualizar_leituras()
