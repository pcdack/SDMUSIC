kugou_search_url_first='http://mobilecdn.kugou.com/api/v3/search/song?keyword='
kugou_search_url_index='&format="json"&page='
kugou_search_url_last='&pagesize=10'
kugou_base_download_url='http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash='
kugou_header = {'Referer': 'http://m.kugou.com/v2/static/html/search.html',
                     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

kugou_lyric='http://m.kugou.com/app/i/krc.php?cmd=100&timelength=999999&hash='


def get_search_url(music_name,page_num):
    return kugou_search_url_first+music_name+kugou_search_url_index+str(page_num)+kugou_search_url_last

def get_lyric_url(music_hash):
    return kugou_lyric+music_hash
