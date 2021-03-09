from apis import CommonRequestWrapper, HTTP_CLIENT, SETTING, RegExpResponseContainer
from urllib import parse
import re


class API:
    file_headers = {'user-agent': 'okhttp/3.10.0'}

    @staticmethod
    def info_url(song_id):
        return "http://www.kuwo.cn/play_detail/{song_id}".format(song_id=song_id)

    @staticmethod
    def file_api(song_id):
        return "http://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&" \
               "rid=MUSIC_{song_id}".format(song_id=song_id)

    @staticmethod
    def search_cookie(keyword):
        return "http://kuwo.cn/search/list?key={keyword}".format(keyword=parse.quote(keyword))

    @staticmethod
    def search_api(keyword, page, pagesize):
        return "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?" \
               "key={keyword}&pn={page}&rn={pagesize}".format(keyword=parse.quote(keyword),
                                                              page=page,
                                                              pagesize=pagesize)
@CommonRequestWrapper
def getMusicInfo(song_id: str):
    """
    get audio info url: web page raw

    :param song_id: song id
    :return: bytes
    """
    return ("get",
            API.info_url(song_id)
            )

@CommonRequestWrapper
def getMusicFile(song_id: str):
    """
    get audio file url

    :param song_id: song id
    :return: bytes
    """
    return ("get",
            API.file_api(song_id),
            {"headers": API.file_headers}
            )

@CommonRequestWrapper
def getSearchResult(keyword, page: int = 1, pagesize: int = 5):
    """
    get search result

    :param keyword: string keywords
    :param page: default value 1, should be integer larger or equal to 1
    :param pagesize: default value 5
    :return: bytes
    """
    token = re.search(r"kw_token=([^\s]*);",
                                     HTTP_CLIENT.get(API.search_cookie(keyword)).headers["Set-Cookie"]).group().split("=")[-1][:-1:]
    return ("get",
            API.search_api(keyword, page, pagesize),
            {"cookies":{"kw_token":token},
             "headers": {"referer": API.search_cookie(keyword),
                         "csrf": token}
             }
            )

# import json
# print(json.dumps(json.loads(getSearchResult("莫愁"))))