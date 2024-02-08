import requests
import os
import alive_progress 
import sys

def remover_repetidos(capitulos:list):
    capitulos_vistos = set()
    capitulos_para_remover = []

    for i, manga in enumerate(capitulos):
        cap = manga['Num_Capitulo']
        if cap in capitulos_vistos:
            capitulos_para_remover.append(i)
        else:
            capitulos_vistos.add(cap)

    # Remover os dicionários da lista
    for indice in reversed(capitulos_para_remover):
        del capitulos[indice]
    
    return capitulos

def baixar_capitulos(capitulos, inicio, fim):
    for i in range(inicio, fim + 1):
        chap_id = capitulos[i]['Id']
        num_chap = capitulos[i]['Num_Capitulo']
        vol_chap = capitulos[i]['Volume']
        
        if vol_chap == None:
            vol_chap = "Nenhum"
        
        chap = requests.get(f"{base_url}/at-home/server/{chap_id}")
        
        r_json = chap.json()

        folder_path = f"/mnt/76C08D67C08D2E85/Mangás/{nome_manga}/Volume {vol_chap}/Capitulo {num_chap}"
        os.makedirs(folder_path, exist_ok=True)
        
        host = r_json["baseUrl"]
        chapter_hash = r_json["chapter"]["hash"]
        data_saver = r_json["chapter"]["dataSaver"]
        data = r_json["chapter"]["data"]

        with alive_progress.alive_bar(len(data_saver), title = f"Capitulo {num_chap} - Vol {vol_chap}") as bar:
            for index, page in enumerate(data_saver):
                if os.path.exists(f"{folder_path}/Page {index}"):
                    continue
                r = requests.get(f"{host}/data/{chapter_hash}/{page}")
                if r.status_code == 404:
                    page = data[index]
                    r = requests.get(f"{host}/data/{chapter_hash}/{page}")
                with open(f"{folder_path}/Page {index}", mode="wb") as f:
                    f.write(r.content)
                bar()
            #print("Cápitulo já existente")

base_url = "https://api.mangadex.org"

languages =['pt-br']

print("\nIniciando conexão com MangaDex\n")

title = sys.argv[1]

r = requests.get(
    f"{base_url}/manga",
    params={"title": title}
)

mangas_achados = [manga for manga in r.json()["data"]]

if len(mangas_achados) != 0:

    for index, m in enumerate(mangas_achados):
        title = m["attributes"]['title']['en']
        print(f"[{index + 1}] - {title}")

    resp = int(input("\nQual mangá deseja selecionar? ")) - 1
    print("\n")
    
    manga_id = mangas_achados[resp]['id']
    nome_manga = mangas_achados[resp]["attributes"]['title']['en']

    r1 = requests.get(f"{base_url}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages})

    limit = r1.json()['total'] if r1.json()['total'] <= 500 else 500


    r2 = requests.get(
        f"{base_url}/manga/{manga_id}/feed",
        params={"translatedLanguage[]": languages, 'limit': limit},
    )

    capitulos = []

    for manga in r2.json()['data']:
        id_capitulo = manga["id"]
        volume_capitulo = manga['attributes']["volume"]
        n_capitulo = manga['attributes']["chapter"]
        titulo_capitulo = manga['attributes']['title']
        capitulos.append({'Num_Capitulo': n_capitulo, 'Id':id_capitulo, 'Titulo': titulo_capitulo, 'Volume':volume_capitulo})

    capitulos_organizados = sorted(capitulos, key=lambda x : float(x['Num_Capitulo']))

    capitulos_sem_repeticao = remover_repetidos(capitulos_organizados)

    for index, cap_vol in enumerate(capitulos_sem_repeticao):
        print(f"({index + 1}) - Capitulo {cap_vol['Num_Capitulo']} - {cap_vol['Titulo']}")

    #* Ajustar para poder escolher os capitulos para baixar

    print(f"\n{len(capitulos_sem_repeticao)} Capitulos encontrados\n")

    escolha_cap = input("Quais capitulos deseja baixar? ")

    if "-" in escolha_cap:
        cap_ini, cap_fim = escolha_cap.split("-")
        baixar_capitulos(capitulos_sem_repeticao, int(cap_ini) - 1, int(cap_fim) - 1)
    elif escolha_cap.isnumeric():
        baixar_capitulos(capitulos_sem_repeticao, int(escolha_cap) - 1, int(escolha_cap) - 1)
    elif escolha_cap == "todos":
        baixar_capitulos(capitulos_sem_repeticao, 0, len(capitulos_sem_repeticao))
    elif escolha_cap == "nenhum":
        print("Nenhum capitulo será baixado")
    else:
        print("opção não existente")
else:
    print("Mangá não encontrado")

