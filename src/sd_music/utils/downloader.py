import os
from urllib.request import urlopen
from tqdm import tqdm
import requests
# 下载工具
from .cover_music import cover_music

def download_musics(musics,output):
    for music in musics:
        print("正在下载:" + music.name)
        download_from_url(music.download_url,output+music.name+".mp3")

def super_download_musics(musics,output):
    for music in musics:
        print("正在下载:"+music.name)
        super_download(music,output)

def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get('Content-Length', -1))
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


def super_download(music_info, output, music_format='.mp3'):
    music = {}
    cover_url = music_info.album_pic_url
    download_url = music_info.download_url
    music_name = music_info.name
    music['album_name'] = music_info.album_name
    music['author'] = music_info.author
    cover_path = output + music_name + ".jpg"
    music_path = output + music_name + music_format
    download_from_url(cover_url, cover_path)
    download_from_url(download_url, music_path)
    cover_music(music_path, cover_path, music)
