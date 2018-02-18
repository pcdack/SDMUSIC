baidu_search_url = 'http://sug.music.baidu.com/info/suggestion?word='
baidu_download_url = 'http://music.baidu.com/data/music/fmlink'

def get_search_url(music_name,page_info):
    return baidu_search_url+music_name+'&version=2&from='+str(page_info)

def get_download_url(music_id):
    return baidu_download_url+'?songIds='+music_id+'&type=flac'

