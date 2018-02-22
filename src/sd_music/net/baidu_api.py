import requests

from ..utils.shower import show_music, show_title, show_out_of_bound
from ..constants.baidu_constants import get_search_url, get_download_url
from ..net.base_api import BaseApi
from ..bean.music import Music

class BaiduCloud(BaseApi):

    __musicid=''
    music = Music()

    def __init__(self,timeout=30):
        BaseApi.__init__(BaseApi(),timeout)
        self.timeout=timeout

    def get_request(self,url):
        r = requests.get(url)
        result = r.json()
        return result

    def get_music_info(self,music_name,page_num):
        search_url = get_search_url(music_name,page_num)
        result = self.get_request(search_url)
        r = result['data']['song']
        return r

    def show_music_infos(self,music_name,page_num):
        result=self.get_music_info(music_name,page_num)
        i = 1
        show_title()
        for res in result:
            show_music(i,music_name,res['artistname'])
            i += 1

    def get_flac_info(self,name):
        name= self.change_name_format(name)
        infos = self.get_music_info(name, 0)
        info = infos[0]
        id=info['songid']
        download_url_r = requests.get(get_download_url(id))
        download_url_r = download_url_r.json()
        if 'data' in download_url_r:
            music_info = download_url_r['data']['songList'][0]
            music_format = music_info['format']
            if music_format == 'flac':
                print('小伙子恭喜你，存在flac格式音乐')
            else:
                print('这个音乐没有flac格式，嘤嘤嘤')
        else:
            print('这个音乐没有flac格式，嘤嘤嘤')

    def change_name_format(self,name):
        if ' ' in name:
            return name.replace(' ', '\ ')

    def get_flac_url(self,name):
        name = self.change_name_format(name)
        infos = self.get_music_info(name, 0)
        info = infos[0]
        self.__musicid=info['songid']
        download_url_r = requests.get(get_download_url(self.__musicid))
        download_url_r = download_url_r.json()
        music_info = download_url_r['data']['songList'][0]
        return music_info['songLink']

    def get_lrc(self):
        download_url_r = requests.get(get_download_url(self.__musicid))
        download_url_r = download_url_r.json()
        music_info = download_url_r['data']['songList'][0]
        return music_info['lrcLink']

    def get_flac_url_and_info(self,name):
        name=self.change_name_format(name)
        infos = self.get_music_info(name, 0)
        info = infos[0]
        self.__musicid = info['songid']
        self.music.id = info['songid']
        download_url_r = requests.get(get_download_url(self.__musicid))
        download_url_r = download_url_r.json()['data']['songList'][0]
        self.music.name = download_url_r['songName']
        self.music.author = download_url_r['artistName']
        self.music.album_name = download_url_r['albumName']
        self.music.album_pic_url = download_url_r['songPicBig']
        self.music.download_url = download_url_r['songLink']
        return self.music



