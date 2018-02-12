import requests

from ..bean.music import Music
from ..net.base_api import BaseApi
from ..constants.oneting_constants import get_music_search_url, oneting_headers, oneting_base_download_url
from ..utils.shower import show_title, show_music


class OneCloud(BaseApi):

    music=Music()

    def __init__(self,timeout=30):
        BaseApi.__init__(BaseApi(),timeout)
        self.timeout=timeout

    def get_request(self,url):
        r = requests.get(url,timeout=self.timeout)
        result = r.json()
        return result

    def get_music_info(self,music_name,page_num):
        page_num-=1
        url = get_music_search_url(music_name, page_num)
        r = self.get_request(url)
        song_file_paths = r['results']
        return song_file_paths

    def show_music_infos(self,music_name,page_mun):
        song_file_paths=self.get_music_info(music_name,page_mun)
        show_title()
        i = 1
        for song_files in song_file_paths:
            author = song_files['singer_name']
            show_music(i,music_name,author)
            i += 1

    def get_music_url_and_info(self,music_name,page_num,index):
        song_file_paths = self.get_music_info(music_name, page_num)
        if len(song_file_paths) >= index:
            song_file = song_file_paths[index]
            download_url = oneting_base_download_url + song_file['song_filepath']
            self.music.name=music_name
            self.music.author=song_file['singer_name']
            self.music.album_name=song_file['album_name']
            self.music.album_pic_url=song_file['album_cover']
            download_url = download_url.replace('wma', 'mp3')
            self.music.download_url=download_url
            return self.music
        else:
            print("索引超出范围")

    def get_music_url(self,music_name,page_num,index):
        song_file_paths = self.get_music_info(music_name, page_num)
        if len(song_file_paths)>=index:
            song_file=song_file_paths[index]
            download_url=oneting_base_download_url+song_file['song_filepath']
            download_url=download_url.replace('wma','mp3')
            return download_url
        else:
            print("索引超出范围")


