import requests

base_url = "https://api.mangadex.org"

languages =['pt-br']


title = "Kanojyo to Himitsu to Koimoyou"

chapter_id = "9a950686-530b-43a0-872a-5871786f669d"

r = requests.get(
    f"{base_url}/manga",
    params={"title": title}
)

manga_id = "c52b2ce3-7f95-469c-96b0-479524fb7a1a"

r1 = requests.get(f"{base_url}/manga/{manga_id}/feed", params={"translatedLanguage[]": languages})

r2 = requests.get(
    f"{base_url}/manga/{manga_id}/feed",
    params={"translatedLanguage[]": languages},
)

#print([chapter["id"] for chapter in r2.json()["data"]])

#print([manga["id"] for manga in r.json()["data"]])

chap = requests.get(f"{base_url}/at-home/server/{chapter_id}")

r_json = chap.json()

host = r_json["baseUrl"]
chapter_hash = r_json["chapter"]["hash"]
data = r_json["chapter"]["data"]
data_saver = r_json["chapter"]["dataSaver"]
