import os
from urllib.request import urlopen
from tqdm import tqdm
import requests
# 下载工具
from .. import config
from .cover_music import cover_music


def download_musics(musics, output, music_format = '.mp3'):
    for music in musics:
        print("正在下载:" + music.name)
        if '/' in music.name:
            music.name = music.name.replace('/', '')
        if music_format == '.m4a':
            song_file_name = '{}.m4a'.format(music.name)
            switcher_song = {
                1: song_file_name,
                2: '{} - {}.m4a'.format(music.author, music.name),
                3: '{} - {}.m4a'.format(music.name, music.author)
            }
        else:
            song_file_name = '{}.mp3'.format(music.name)
            switcher_song = {
                1: song_file_name,
                2: '{} - {}.mp3'.format(music.author, music.name),
                3: '{} - {}.mp3'.format(music.name, music.author)
            }
        song_file_name = switcher_song.get(config.SONG_NAME_TYPE, song_file_name)
        download_from_url(music.download_url, output+song_file_name)


def super_download_musics(musics, output, music_format='.mp3'):
    for music in musics:
        print("正在下载:"+music.name)
        super_download(music, output, music_format)


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
    if '/' in music_name:
        music_name = music_name.replace('/', '')
    music['album_name'] = music_info.album_name
    music['author'] = music_info.author
    if music_format == '.m4a':
        song_file_name = '{}.m4a'.format(music_info.name)
        switcher_song = {
            1: song_file_name,
            2: '{} - {}.m4a'.format(music_info.author, music_info.name),
            3: '{} - {}.m4a'.format(music_info.name, music_info.author)
        }
    elif music_format == '.flac':
        song_file_name = '{}.flac'.format(music_info.name)
        switcher_song = {
            1: song_file_name,
            2: '{} - {}.flac'.format(music_info.author, music_info.name),
            3: '{} - {}.flac'.format(music_info.name, music_info.author)
        }
    else:
        song_file_name = '{}.mp3'.format(music_info.name)
        switcher_song = {
            1: song_file_name,
            2: '{} - {}.mp3'.format(music_info.author, music_info.name),
            3: '{} - {}.mp3'.format(music_info.name, music_info.author)
        }
    song_file_name = switcher_song.get(config.SONG_NAME_TYPE, song_file_name)
    cover_path = output + music_name + ".jpg"
    music_path = output + song_file_name
    download_from_url(cover_url, cover_path)
    download_from_url(download_url, music_path)
    cover_music(music_path, cover_path, music)
