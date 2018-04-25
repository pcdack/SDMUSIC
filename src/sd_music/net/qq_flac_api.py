import requests
import json
import tqdm
from ..constants.qqmusic_constants import qq_music_flac_info_url, qq_headers, quality
from ..net.base_api import BaseApi

class QQFlacCloud(BaseApi):
    def __init__(self,timeout=30):
        BaseApi.__init__(BaseApi(), timeout)
        self.timeout = timeout

    def get_request(self,url,header):
        r=requests.get(url,headers=header,timeout=self.timeout)
        result=r.json()
        if result['code'] != 0:
            print('Error return{} when try to use get function{}'.format(result,url))
        else:
            return result

    def get_info(self,music_name,pernum=20,p=0):
        music_search_url = qq_music_flac_info_url(music_name, pernum,p)
        r = requests.get(music_search_url, qq_headers)
        jm = json.loads(r.text.strip('callback()[]'))
        return jm['data']['song']

    def check_music_flac(self,music_name):
        pernum=10
        quality_type = 'flac'
        data=self.get_info(music_name)
        total_num=data['totalnum']
        print(f'正在抓取关键词>>{music_name}<<的基本信息，共有{total_num}首歌')
        jm1 = []
        end_num = max(2, total_num // pernum + 1)
        for p in tqdm.tqdm(range(1, end_num)):
            jm = self.get_info(music_name, pernum=20, p=p)
            jm0 = jm['list']
            jm1.extend(jm0)
        json_jm = json.dumps(jm1)
        jm1 = [j for j in jm1 if j[quality[quality_type]['size']] != 0]
        [j.update({'quality_type': quality_type}) for j in jm1]
        return  json_jm,jm1

    def get_all_flac_url(self,jm1):
        print('正在抓取flac文件的url')
        for j in tqdm.tqdm(jm1):
            songmid = j['songmid']
            media_mid = j['media_mid']
            res2url = f"https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?" \
                      f"&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=" \
                      f"{songmid}&filename=C400{media_mid}.m4a&guid=6612300644"
            res2 = requests.get(res2url)
            jm2 = json.loads(res2.text)
            vkey = jm2['data']['items'][0]['vkey']
            dl_url = {}
            for dl_type in quality:
                prefix = quality[dl_type]['prefix']
                suffix = quality[dl_type]['suffix']
                dl_url.update({dl_type: f"http://dl.stream.qqmusic.qq.com/{prefix}{media_mid}.{suffix}?vkey={vkey}&guid=6612300644&uin=0&fromtag=53"})
            j.update({'dl_url': dl_url})
        return jm1
