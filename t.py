import mangadex

api = mangadex.Api()
manga_list = api.get_manga_list(title = "Jujutsu Kaisen")
#login = api.login(username="yagohenriquev123@gmail.com", password="yago0211")

manga = api.view_manga_by_id("c52b2ce3-7f95-469c-96b0-479524fb7a1a")

manga_feed = api.manga_feed("c52b2ce3-7f95-469c-96b0-479524fb7a1a", limit = 1)

#a  = api.get_manga_volumes_and_chapters("the manga id")

chapter = api.get_chapter("c52b2ce3-7f95-469c-96b0-479524fb7a1a")
