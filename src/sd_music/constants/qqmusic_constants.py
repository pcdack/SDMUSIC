
qq_search_url_first='https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?w='
qq_search_url_index='&p='
qq_search_url_last='&n=10&format=json'
qq_lyric_url='http://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?format=json&nobase64=1&songtype=0&callback=c&songmid='
qq_album_url='http://y.gtimg.cn/music/photo_new/T002R300x300M000'
qq_download_base_url='https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg'

qq_headers={
'referer': 'https://m.y.qq.com/#search',
'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

qq_lrc_headers={
'referer': 'https://m.y.qq.com/',
'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

def qq_get_music_info_url(music_name,page_num):
    return qq_search_url_first+music_name+qq_search_url_index+str(page_num)+qq_search_url_last

def qq_get_music_lyric_url(msongId):
    return qq_lyric_url+msongId
