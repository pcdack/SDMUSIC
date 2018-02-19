from pydub import AudioSegment
import os
# music_info是一个字典
def export_fun(song,music_path, cover_path, music_info):
    print("此过程需要需要10s左右的时间请耐心等待")
    song.export(music_path,
                tags={'album': music_info['album_name'], 'artist': music_info['author']}
                , format="mp3"
                , cover=cover_path)

def cover_music(music_path, cover_path, music_info):
    if '.mp3' in music_path:
        song=AudioSegment.from_mp3(music_path)
        export_fun(song,music_path,cover_path,music_info)
        os.remove(cover_path)
    elif '.m4a' in music_path:
        song=AudioSegment.from_file(music_path,'m4a')
        music_path=music_path.replace(".m4a",".mp3")
        export_fun(song,music_path,cover_path,music_info)
        music_path = music_path.replace(".mp3", ".m4a")
        os.remove(music_path)
        os.remove(cover_path)
    elif '.flac' in music_path:
        song=AudioSegment.from_file(music_path,'flac')
        export_fun(song,music_path,cover_path,music_info)
