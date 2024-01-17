from googlesearch import search


class MovieLinkSearchEngine():
    async def find_movie(self, title, is_anime = False):
        if is_anime:
            res = tuple(search(f'watch online {title}'))
            res = res[0] if res else 'N/A'
        else:
            res = tuple(search(f'just watch {title}'))
            res = res[0] if res else 'N/A'

        return res
        