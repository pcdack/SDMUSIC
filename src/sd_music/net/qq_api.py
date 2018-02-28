import requests
import json
from tqdm import tqdm

from ..bean.music import Music
from ..constants.qqmusic_constants import qq_headers, qq_get_music_info_url, qq_download_base_url, \
    qq_get_music_lyric_url, qq_lrc_headers, qq_album_url, qq_music_list_url, qq_top_list_url
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_title


class QQMusic(BaseApi):
    __songmId = ''
    music=Music()

    def __init__(self, timeout=30):
        BaseApi.__init__(BaseApi(), timeout)
        self.timeout = timeout

    def get_request(self,url,header):
        r=requests.get(url,headers=header,timeout=self.timeout)
        result=r.json()
        if result['code'] != 0:
            print('Error return{} when try to use get function{}'.format(result,url))
        else:
            return result

    def get_music_info(self,music_name,page_num):
        music_search_url = qq_get_music_info_url(music_name, page_num)
        r = self.get_request(music_search_url, qq_headers)
        myDatas = r['data']['song']['list']
        return myDatas

    def show_music_infos(self, music_name, page_num=1):
        myDatas=self.get_music_info(music_name, page_num)
        show_title()
        i=1
        for m in myDatas:
            authors = m['singer']
            author = ''
            for a in authors:
                author += a['name']
            show_music(i,music_name,author)
            i += 1

    def get_music_url_and_info(self, music_name, index, page_num=1):
        myDatas = self.get_music_info(music_name, page_num)
        data = myDatas[index]
        music = self.get_music_info_by_data(data, self.music)
        return music

    def get_music_url(self, music_name, index, page_num=1):
        myDatas = self.get_music_info(music_name, page_num)
        data=myDatas[index]
        if 'songmid' in data and 'songid' in data:
            mymId = data['songmid']
            myId=data['songid']
            qq_download_url = qq_download_base_url + '?songmid=' + mymId + '&format=json'
            r=self.get_request(qq_download_url,header=qq_headers)
            if 'url' in r:
                download_url = r['url'][str(myId)]
                return "http://"+download_url
            else:
                print("未知错误")
        else:
            print("超出边界")

    def get_music_top_list(self, music_top_id,music_num=100):
        url = qq_top_list_url(music_top_id)
        info = self.get_request(url, qq_headers)
        musics = []
        bar = tqdm(range(music_num))
        infos = info['songlist']
        for music_info in infos:
            music_info = music_info['data']
            music = Music()
            music = self.get_music_info_by_data(music_info, music)
            musics.append(music)
            bar.update(1)
        return musics

    def get_music_list_infos(self, music_list_id):
        url = qq_music_list_url(music_list_id)
        info = self.get_request(url, qq_headers)
        musics = []
        infos = info['cdlist'][0]['songlist']
        for music_info in infos:
            music = Music()
            music.name = music_info['name']
            myId = music_info['id']
            music.id = music_info['mid']
            self.__songmId = music.id
            music.lrc_url = self.get_music_lyric()
            authors = music_info['singer']
            author = ''
            for a in authors:
                author += a['name']
            music.author = author
            album = music_info['album']
            music.album_name = album['name']
            album_id = album['mid']
            music.album_pic_url = qq_album_url+album_id+'.jpg'
            qq_download_url = qq_download_base_url + '?songmid=' + music.id + '&format=json'
            r = self.get_request(qq_download_url, header=qq_headers)
            if 'url' in r:
                download_url = r['url'][str(myId)]
                music.download_url = "http://" + download_url
            else:
                print("未知错误")
            musics.append(music)
        return musics

    def get_music_lyric(self):
        if self.__songmId != '':
            lrc_url = qq_get_music_lyric_url(self.__songmId)
            r = requests.get(lrc_url, headers=qq_lrc_headers)
            lrc = r.text.replace("c(", "").replace(")", "")
            lrc_json = json.loads(lrc)
            if 'lyric' in lrc_json:
                lrc = lrc_json['lyric']
                lrc = lrc.replace("&#58;", ":").replace("&#46;", ":").replace("&#10;", "\n").replace("&#32;",
                                                                                                     " ").replace(
                    "&#45;", "").replace("&#13", "")
            return lrc
        else:
            print("异常")

    def get_music_info_by_data(self, data, music):
        if 'songmid' in data and 'songid' in data:
            mymId = data['songmid']
            myId = data['songid']
            music.name = data['songname']
            authors = data['singer']
            author = ''
            for a in authors:
                author += a['name']
            music.id = mymId
            music.author = author
            music.album_name = data['albumname']
            self.__songmId = mymId
            music.lrc_url = self.get_music_lyric()
            music.album_pic_url = qq_album_url + data['albummid'] + '.jpg'
            qq_download_url = qq_download_base_url + '?songmid=' + mymId + '&format=json'
            r = self.get_request(qq_download_url, header=qq_headers)
            if 'url' in r:
                download_url = r['url'][str(myId)]
                music.download_url = "http://" + download_url
                return music
        else:
            print("未知错误")