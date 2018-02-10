
qq_search_url_first='https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?w='
qq_search_url_index='&p='
qq_search_url_last='&n=10&format=json'

qq_download_base_url='https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg'

qq_headers={
'referer': 'https://m.y.qq.com/#search',
'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

def qq_get_music_info_url(music_name,page_num):
    return qq_search_url_first+music_name+qq_search_url_index+str(page_num)+qq_search_url_last

