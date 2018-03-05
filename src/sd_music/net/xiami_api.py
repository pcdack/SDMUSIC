import requests

import json
import re
from ..bean.music import Music
from ..constants.xiami_constants import get_search_url, xiami_header, get_list_url, get_hot_url, get_music_id
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_out_of_bound


class XiaMiCloud(BaseApi):
    __lrcurl = ''
    music = Music()

    def __init__(self, timeout=30):
        BaseApi.__init__(BaseApi(), timeout)
        self.timeout = timeout

    def get_request(self,url,header):
        r = requests.get(url, headers=header, timeout=self.timeout)
        if 'jsonp' in r.text:
            m = re.match('jsonp\d{3}\((.*)\).*$', r.text)
            result = json.loads(str(m.group(1)))
        else:
            result = r.json()
        if result['state'] != 0:
            print('Error return{} when try to use get function{}'.format(result,url))
        else:
            return result

    def get_music_info(self,music_name,page_num):
        url = get_search_url(music_name, page_num)
        r = self.get_request(url, xiami_header)
        infos = r['data']['songs']
        return infos

    def show_music_infos(self,music_name,page_num):
        infos=self.get_music_info(music_name,page_num)
        i=1
        for info in infos:
            author = info['artist_name']
            show_music(i,music_name,author)
            i+=1

    def get_music_url_and_info(self,music_name,page_num,index):
        infos = self.get_music_info(music_name, page_num)
        if len(infos) >= index:
            info = infos[index]
            self.music.name=music_name
            self.music.author=info['artist_name']
            self.music.album_name=info['album_name']
            self.music.album_pic_url=info['album_logo']
            self.music.download_url=info['listen_file']
            return self.music
        else:
            show_out_of_bound()

    def get_music_url(self,music_name,page_num,index):
        infos = self.get_music_info(music_name,page_num)
        if len(infos) >= index:
            info=infos[index]
            download_url = info['listen_file']
            self.__lrcurl = info['lyric']
            return download_url
        else:
            show_out_of_bound()

    def get_music_lrc_url(self):
        return self.__lrcurl

    def get_play_list(self, music_list_id):
        musics = []
        get_play_list_url = get_list_url(music_list_id)
        result = self.get_request(get_play_list_url, xiami_header)
        datas = result['data']['songs']
        for data in datas:
            music = Music()
            music.name = data['song_name']
            music.author = data['artist_name']
            music.album_name = data['album_name']
            music.album_pic_url = data['album_logo']
            music.id = data['song_id']
            music.download_url = data['listen_file']
            music.lrc_url = data['lyric']
            musics.append(music)
        return musics

    def get_music_info_by_id(self,music_id,music):
        url = get_music_id(music_id)
        result = self.get_request(url, xiami_header)
        data = result['data']['song']
        music.name = data['song_name']
        music.album_name = data['album_name']
        music.album_pic_url = data['logo']
        music.lrc_url = data['lyric']
        music.author = data['singers']
        music.download_url=data['listen_file']

    def get_hot_music_infos(self, hot_music_id):
        musics = []
        #todo 通过config文件配置指定下载数量
        hot_music_url = get_hot_url(hot_music_id, 1)
        result = self.get_request(hot_music_url, xiami_header)
        datas = result['data']
        for data in datas:
            music = Music()
            id = data['song_id']
            self.get_music_info_by_id(id, music)
            musics.append(music)
        return musics