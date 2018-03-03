xiami_search_url_first='http://api.xiami.com/web?key='
xiami_search_url_index='&v=2.0&app_key=1&r=search/songs&page='
xiami_search_url_last='&limit=10'
xiami_header = {'Referer': 'http://m.xiami.com/',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
xiami_list_url = 'http://api.xiami.com/web?v=2.0&app_key=1&id='
xiami_id_url = 'http://api.xiami.com/web?v=2.0&app_key=1&id='
xiami_dict = {'hot': 101, 'origin': 103}


def get_search_url(music_name,page_num):
    return xiami_search_url_first+music_name+xiami_search_url_index+str(page_num)+xiami_search_url_last


def get_list_url(music_play_list_id):
    return xiami_list_url+str(music_play_list_id)+'&_ksTS=1519178637805_181&callback=jsonp182&r=collect/detail'


def get_hot_url(hot_music, page_num):
    return xiami_list_url+str(hot_music)+'&page='+str(page_num)+ '&limit=20&_ksTS=1519178960838_236&callback=jsonp237&r=rank/song-list'


def get_music_id(music_id):
    return xiami_id_url + str(music_id)+'&_ksTS=1519879890812_170&callback=jsonp171&r=song/detail'