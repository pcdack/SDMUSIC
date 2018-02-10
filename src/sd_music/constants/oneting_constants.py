oneting_search_first='http://so.1ting.com/song/json?q='
oneting_search_index='&type=1&offset='
oneting_search_last='&limit=10'
oneting_base_download_url='http://96.1ting.com'
oneting_headers={
'referer': 'http://so.1ting.com/',
'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}

def get_music_search_url(music_name,page_num):
    return oneting_search_first+music_name+oneting_search_index+str(page_num)+oneting_search_last

