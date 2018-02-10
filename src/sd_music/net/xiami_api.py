import requests

from ..constants.xiami_constants import get_search_url, xiami_header
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_out_of_bound


class XiaMiCloud(BaseApi):
    def __init__(self, timeout=30):
        BaseApi.__init__(BaseApi(), timeout)
        self.timeout = timeout

    def get_request(self,url,header):
        r=requests.get(url,headers=header,timeout=self.timeout)
        result=r.json()
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

    def get_music_url(self,music_name,page_num,index):
        infos=self.get_music_info(music_name,page_num)
        if len(infos)>=index:
            info=infos[index]
            download_url = info['listen_file']
            return download_url
        else:
            show_out_of_bound()
