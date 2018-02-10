import requests

from ..constants.kugou_constants import get_search_url, kugou_header, kugou_base_download_url
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_out_of_bound, show_title


class KugouCloud(BaseApi):
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
        infos=self.get_music_info(music_name,page_num)
        if len(infos) >= index:
            info=infos[index]
            hash_code = info['hash']
            get_download_url=kugou_base_download_url+hash_code
            download_r=self.get_request(get_download_url,header=kugou_header)
            download_url=download_r['url']
            return download_url
        else:
            show_out_of_bound()



