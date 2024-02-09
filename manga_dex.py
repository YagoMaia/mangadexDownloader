import requests
import os
import alive_progress 
import sys
import json

base_url = "https://api.mangadex.org"
path_atual = os.path.dirname(os.path.realpath(__file__))

languages =['pt-br']

#* Mangas no Json Mangas Diários

def json_mangas_diarios():
    
    if os.path.exists(f"{path_atual}/mangas_diarios.json"):
        with open(f"{path_atual}/mangas_diarios.json", "r") as mangas_diarios:
            data = json.load(mangas_diarios)
    else:
        data = {"Atuais":[]}
        with open(f"{path_atual}/mangas_diarios.json", "w+") as mangas_diarios:
            json.dump(data, mangas_diarios)
    return data

def adicionar_manga_diario(data:dict):
    
    repetido = False
    
    mangas_atuais = json_mangas_diarios()
    for m in mangas_atuais['Atuais']:
        if m['Titulo'] == data['Titulo']:
            repetido = True
    if repetido == False:
        mangas_atuais['Atuais'].append(data)
        
        with open(f"{path_atual}/mangas_diarios.json", "w") as ponteiro_json:
            json.dump(mangas_atuais, ponteiro_json)
        print(f"\nMangá {data['Titulo']} adicionado na lista de mangás Atuais")
    else:
        print("\nMangá repetido")

def remover_manga_diario(indice : int):
    
    mangas_atuais = json_mangas_diarios()
    mangas_atuais['Atuais'].pop(indice)
    with open(f"{path_atual}/mangas_diarios.json", "w") as ponteiro_json:
        json.dump(mangas_atuais, ponteiro_json)
    print("\nMangá removido")
        
def listar_mangas_diarios():
    
    mangas_atuais = json_mangas_diarios()
    print("\nMangas na lista de atuais\n")
    for index, m in enumerate(mangas_atuais['Atuais']):
        print(f"{index+1} - {m['Titulo']}")

#* Funções para baixar capitulos e mostrar mangás disponíveis

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
                if not os.path.exists(f"{folder_path}/Page {index}"):
                    r = requests.get(f"{host}/data-saver/{chapter_hash}/{page}")
                    if r.status_code == 404:
                        page = data[index]
                        r = requests.get(f"{host}/data/{chapter_hash}/{page}")
                    with open(f"{folder_path}/Page {index}", mode="wb") as f:
                        f.write(r.content)
                bar()
            #print("Cápitulo já existente")

def listar_mangas(titulo_manga):
    r = requests.get(f"{base_url}/manga", params={"title": titulo_manga})

    mangas_achados = [manga for manga in r.json()["data"]]

    if len(mangas_achados) != 0:

        for index, m in enumerate(mangas_achados):
            title = m["attributes"]['title']['en']
            print(f"[{index + 1}] - {title}")

        resp = int(input("\nQual mangá deseja selecionar? ")) - 1
        
        titulo_manga_selecionado = mangas_achados[resp]['attributes']['title']['en']
        
        return mangas_achados[resp], f"\n{titulo_manga_selecionado} selecionado"
    return None, "\nMangá não encontrado"

title = sys.argv[1]

match title:
    case "diario":
        a = json_mangas_diarios()
    
    case "adicionar":
        nome_manga = sys.argv[2]
        manga_selecionado, mensagem = listar_mangas(nome_manga)
        print(mensagem)
        if manga_selecionado is not None:
            manga_id = manga_selecionado['id']
            nome_manga = manga_selecionado["attributes"]['title']['en']
            novo_manga = {'Titulo':nome_manga, 'Id': manga_id}
            adicionar_manga_diario(novo_manga)
    
    case "remover":
        numero_manga = int(sys.argv[2])
        remover_manga_diario(numero_manga - 1)
        
    case "listar":
        listar_mangas_diarios()
    
    case _:
        print("\nIniciando conexão com MangaDex\n")
        manga_selecionado, mensagem = listar_mangas(title)
        print(mensagem)
        if manga_selecionado is not None:
        
            manga_id = manga_selecionado['id']
            nome_manga = manga_selecionado["attributes"]['title']['en']
            # ultima_cap_add = manga_selecionado["attributes"]['attributes']['latestUploadedChapter']
            
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
            print("\n")
            
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

