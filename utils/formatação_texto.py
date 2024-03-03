import pyfiglet


def generate_ascii_art(texto: str) -> str:
    """
    Função responsável por gerar um text ascii art.

    Parâmetro:
        texto : str -> Texto que será fetio a ascii art
    """
    ascii_art = pyfiglet.figlet_format(texto)
    return ascii_art
