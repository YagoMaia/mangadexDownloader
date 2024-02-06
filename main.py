# Import the MangaDexPy library
import MangaDexPy
cli = MangaDexPy.MangaDex()
#cli.login("yagohenriquev123@gmail.com", "yago0211")

# Get manga with id b9797c5b-642e-44d9-ac40-8b31b9ae110a.
manga = cli.get_manga("237d527f-adb5-420e-8e6e-b7dd006fbe47")

print(manga.title + "'s latest volume:")
print(manga.last_volume)
print(manga.title + "'s latest chapter:")
print(manga.last_chapter)