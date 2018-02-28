
qq_search_url_first='https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?w='
qq_search_url_index='&p='
qq_search_url_last='&n=10&format=json'
qq_lyric_url='http://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?format=json&nobase64=1&songtype=0&callback=c&songmid='
qq_album_url='http://y.gtimg.cn/music/photo_new/T002R300x300M000'
qq_download_base_url='https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg'
qq_list_url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&new_format=1&pic=500&disstid='
qq_top_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&tpl=3&page=detail&type=top&topid='

qq_headers={
'referer': 'https://m.y.qq.com/#search',
'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

qq_lrc_headers={
'referer': 'https://m.y.qq.com/',
'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

qq_dict = {'soar': 4, 'hot': 26, 'new': 27}


def qq_get_music_info_url(music_name,page_num):
    return qq_search_url_first+music_name+qq_search_url_index+str(page_num)+qq_search_url_last


def qq_get_music_lyric_url(msongId):
    return qq_lyric_url+msongId


def qq_music_list_url(listId):
    return qq_list_url+str(listId)+'&type=1&json=1&utf8=1&onlysong=0&picmid=1&nosign=1&song_begin=0&song_num=15&_=1519445320400'


def qq_top_list_url(topId):
    return qq_top_url+str(topId)+'&_=1519445015470'