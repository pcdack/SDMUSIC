import requests
from ..constants.qqmusic_constants import qq_headers, qq_get_music_info_url, qq_download_base_url
from ..net.base_api import BaseApi
from ..utils.shower import show_music, show_title


class QQMusic(BaseApi):
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

    def show_music_infos(self,music_name,page_num=1):
        myDatas=self.get_music_info(music_name,page_num)
        show_title()
        i=1
        for m in myDatas:
            authors = m['singer']
            author = ''
            for a in authors:
                author += a['name']
            show_music(i,music_name,author)
            i += 1


    def get_music_url(self,music_name,index,page_num=1):
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
