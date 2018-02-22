import requests

from ..bean.music import Music
from ..constants.kugou_constants import get_search_url, kugou_header, kugou_base_download_url,get_lyric_url
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_out_of_bound, show_title


class KugouCloud(BaseApi):
    __hash=''
    music=Music()

    def __init__(self,timeout=30):
        BaseApi.__init__(BaseApi(),timeout)
        self.timeout=timeout

    def get_request(self,url,header):
        r=requests.get(url,headers=header,timeout=self.timeout)
        result=r.json()
        if result['status'] != 1:
            print('Error return{} when try to use get function{}'.format(result,url))
        else:
            return result

    def get_music_info(self,music_name,page_num):
        url=get_search_url(music_name,page_num)
        r=self.get_request(url,kugou_header)
        infos=r['data']['info']
        return infos

    def show_music_infos(self,music_name,page_num):
        infos=self.get_music_info(music_name,page_num)
        show_title()
        i=1
        for info in infos:
            authors=info['singername']
            music_name=info['songname_original']
            show_music(i,music_name,authors)
            i+=1

    def get_music_url(self,music_name,page_num,index):
        infos = self.get_music_info(music_name, page_num)
        if len(infos) >= index:
            info = infos[index]
            hash_code = info['hash']
            self.__hash = hash_code
            get_download_url = kugou_base_download_url + hash_code
            download_r = self.get_request(get_download_url, header=kugou_header)
            download_url = download_r['url']
            return download_url
        else:
            show_out_of_bound()

    def get_music_url_and_info(self,music_name,page_num,index):
        infos=self.get_music_info(music_name,page_num)
        if len(infos) >= index:
            info=infos[index]
            hash_code = info['hash']
            self.__hash=hash_code
            get_download_url=kugou_base_download_url+hash_code
            download_r=self.get_request(get_download_url,header=kugou_header)
            self.music.name=download_r['songName']
            self.music.album_name=download_r['fileName']
            self.music.album_pic_url=download_r['album_img'].replace("{size}","150")
            self.music.download_url=download_r['url']
            self.music.author=download_r['choricSinger']
            return self.music
        else:
            show_out_of_bound()

    def get_music_lyric(self):
        hash_code=self.__hash
        lyric_url=get_lyric_url(hash_code)
        r=requests.get(lyric_url)
        lrc=r.text.encode('iso-8859-1').decode('utf-8').replace("\r","")
        return lrc


