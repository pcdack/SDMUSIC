import requests

from ..constants.netease_constants import headers, get_song_url, netease_music_search_url,netease_song_download_url
from ..encrypt.netease_encrypt import encrypted_request
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_title


class NetEaseCloud(BaseApi):
    def __init__(self,timeout=30):
        BaseApi.__init__(BaseApi(),timeout)
        self.timeout=timeout


    def post_request(self,url,params):
        data =encrypted_request(params)
        r=requests.post(url,data=data,headers=headers,timeout=self.timeout)
        result=r.json()
        if result['code'] != 200:
            print('Error return {} when try to post {} => {}'.format(result,data,url))
        else:
            return result

    def get_song(self, song_id):
        """
        Get song info by song id
        :param song_id:
        :return:
        """
        url = get_song_url(song_id)
        result = self.common_get_request(url,headers)

        return result['songs'][0]
    def get_music_url(self, song_id, bit_rate=320000):
        """Get a song's download url.
        :params song_id: song id<int>.
        :params bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
        :return:
        """
        url = netease_song_download_url
        csrf = ''
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        result = self.post_request(url, params)
        song_url = result['data'][0]['url']
        return song_url

    def get_music_id_json(self,music_name,offset):
        url=netease_music_search_url
        params={'s':music_name,'type':1,'offset':offset,'limit':10}
        result=self.common_post_request(url,headers,params)
        if 'songs' in result['result']:
            return result['result']['songs']


    def get_music_ids(self,music_name,offset=1):
        myIdJsons = self.get_music_id_json(music_name, offset)
        myIds=[]
        for myIdJson in myIdJsons:
            myId=myIdJson['id']
            myIds.append(myId)
        return myIds

    # 获取音乐的作者和MusicId
    def get_musics_info(self,music_name,offset=1):
        myIdJsons=self.get_music_id_json(music_name,offset)
        music_infos=[]
        index=1
        if myIdJsons != None:
            for myIdJson in myIdJsons:
                music_info = {}
                myId = myIdJson['id']
                myAuthors=myIdJson['ar']
                authors = ''
                for author in myAuthors:
                    authors += author['name']
                music_info['author']=authors
                music_info['id']=myId
                music_info['music_name']=music_name
                music_info['index']=index
                music_infos.append(music_info)
                index+=1
            return music_infos
        else:
            print("出现错误")
    def show_music_info(self,music_name,offset=1):
        music_infos=self.get_musics_info(music_name,offset)
        if music_infos != None:
            show_title()
            for music_info in music_infos:
                show_music(music_info['index'],music_info['music_name'],music_info['author'])
                # print(str(music_info['index'])+"\t"+music_info['music_name']+"\t"+music_info['author'])
        else:
            print("出现错误")

    # 获取音乐直链
    def get_music_download_url(self,selected_id):
        music=self.get_song(selected_id)
        song_id=music['id']
        music_url=self.get_music_url(song_id)
        return music_url