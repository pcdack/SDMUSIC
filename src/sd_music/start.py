import argparse
from urllib.parse import parse_qs, urlparse

from .constants.qqmusic_constants import qq_dict
from .constants.netease_constants import netease_dict
from .constants.xiami_constants import xiami_dict
from . import config
from .net.baidu_api import BaiduCloud
from .net.kugou_api import KugouCloud
from .net.netease_api import NetEaseCloud
from .net.oneting_api import OneCloud
from .net.qq_api import QQMusic
from .net.xiami_api import XiaMiCloud
from .utils.downloader import download_from_url, super_download, download_musics, super_download_musics

desc="Search && Download Music cli"
version_info="""
 ______     _____     __    __     __  __     ______     __     ______    
/\  ___\   /\  __-.  /\ "-./  \   /\ \/\ \   /\  ___\   /\ \   /\  ___\   
\ \___  \  \ \ \/\ \ \ \ \-./\ \  \ \ \_\ \  \ \___  \  \ \ \  \ \ \____  
 \/\_____\  \ \____-  \ \_\ \ \_\  \ \_____\  \/\_____\  \ \_\  \ \_____\ 
  \/_____/   \/____/   \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_____/
  
Search && Download Music Cli
version 0.11a 
"""

config.load_config()


def w_lrc(output,music_name,lrc):
    with open(output + music_name + ".lrc", "w") as f:
        f.write(lrc)


def format_music_name(song_file_name):
    if '/' in song_file_name:
        song_file_name = song_file_name.replace('/', '')
    return song_file_name


def get_music_name(music_info, music_format='.mp3'):

    if music_format == '.m4a':
        song_file_name = '{}.m4a'.format(music_info.name)
        switcher_song = {
            1: song_file_name,
            2: '{} - {}.m4a'.format(music_info.author, music_info.name),
            3: '{} - {}.m4a'.format(music_info.name, music_info.author)
        }
    else:
        song_file_name = '{}.mp3'.format(music_info.name)
        switcher_song = {
            1: song_file_name,
            2: '{} - {}.mp3'.format(music_info.author, music_info.name),
            3: '{} - {}.mp3'.format(music_info.name, music_info.author)
        }
    song_file_name = switcher_song.get(config.SONG_NAME_TYPE, song_file_name)
    print(song_file_name)
    return song_file_name


def search_or_download(music_name, offset, platfrom='netease', choose=True, index=1, output='./', lyric=False, album=False):
    if platfrom == 'netease':
        net_api=NetEaseCloud()
        if choose:
            net_api.show_music_info(music_name,offset)
        else:
            mIds = net_api.get_music_ids(music_name, offset)
            id = mIds[index]
            music_info = net_api.get_music_download_info(id)
            song_file_name = format_music_name(get_music_name(music_info))
            if album:
                super_download(music_info, output)
            else:
                download_from_url(music_info.download_url, output+song_file_name)
            if lyric:
                lry=net_api.get_music_lyric(id)
                w_lrc(output,music_name,lry)
    elif platfrom == 'qq':
        qq_api=QQMusic()
        if choose:
            qq_api.show_music_infos(music_name, offset)
        else:
            music_info = qq_api.get_music_url_and_info(music_name, index, offset)
            song_file_name = format_music_name(get_music_name(music_info, '.m4a'))
            if album:
                super_download(music_info, output, ".m4a")
            else:
                download_from_url(music_info.download_url, output+song_file_name)
            if lyric:
                lrc = music_info.lrc_url
                w_lrc(output, music_name, lrc)
        pass
    elif platfrom == '1ting':
        oneting_api=OneCloud()
        if choose:
            oneting_api.show_music_infos(music_name, offset)
        else:
            music_info = oneting_api.get_music_url_and_info(music_name, offset, index)
            song_file_name = format_music_name(get_music_name(music_info))
            if album:
                super_download(music_info, output)
            else:
                download_from_url(music_info.download_url, output+song_file_name)
        pass
    elif platfrom == 'xiami':
        xiami_api=XiaMiCloud()
        if choose:
            xiami_api.show_music_infos(music_name,offset)
        else:
            music_info = xiami_api.get_music_url_and_info(music_name, offset, index)
            song_file_name = format_music_name(get_music_name(music_info))
            if album:
                super_download(music_info,output)
            else:
                download_from_url(music_info.download_url, output+song_file_name)
            if lyric:
                download_from_url(xiami_api.get_music_lrc_url(),output+music_name+'.trc')
        pass
    elif platfrom == 'kugou':
        kugou_api=KugouCloud()
        if choose:
            kugou_api.show_music_infos(music_name,offset)
        else:
            music_info = kugou_api.get_music_url_and_info(music_name, offset, index)
            song_file_name = format_music_name(get_music_name(music_info))
            if album:
                super_download(music_info,output)
            else:
                download_from_url(music_info.download_url, output+song_file_name)
            if lyric:
                lrc=kugou_api.get_music_lyric()
                w_lrc(output, music_name, lrc)
        pass


def download_netease_playlist_songs(music_play_list, output, lrc=False, album=False):
    net_api = NetEaseCloud()
    musics = net_api.get_play_list(music_play_list)
    if album:
        super_download_musics(musics, output)
    else:
        download_musics(musics, output)
    if lrc:
        for music in musics:
            lry = net_api.get_music_lyric(music.id)
            w_lrc(output, music.name, lry)


def download_qq_hot_songs(id, output, lyric, album):
    print("数据有点多，有300首左右，请稍等。。。嘤嘤嘤,下面是加载进度条，不是下载进度")
    qq_api = QQMusic()
    qq_musics = qq_api.get_music_top_list(id, 300)
    if album:
        super_download_musics(qq_musics, output)
    else:
        download_musics(qq_musics, output)
    if lyric:
        for music in qq_musics:
            lrc = music.lrc_url
            if lrc:
                w_lrc(output, music.name, lrc)
            else:
                print("没有歌词!")
    pass


def download_xiami_hot_songs(id, output, lyric, album):
    xiami_api = XiaMiCloud()
    xiami_musics = xiami_api.get_hot_music_infos(id)
    if album:
        super_download_musics(xiami_musics, output)
    else:
        download_musics(xiami_musics, output)
    if lyric:
        for music in xiami_musics:
            lrc_url = music.lrc_url
            download_from_url(lrc_url, output + music.name + '.trc')


def download_xiami_playlist_songs(music_play_list,output,lrc=False,album=False):
    xiami = XiaMiCloud()
    musics = xiami.get_play_list(music_play_list)
    if album:
        super_download_musics(musics, output)
    else:
        download_musics(musics, output)
    if lrc:
        for music in musics:
            lrc = music.lrc_url
            if lrc:
                download_from_url(lrc, output + music.name + '.trc')
            else:
                print("没有歌词!")


def download_qq_playlist_songs(id, output, lyric=False, album=False):
    qq = QQMusic()
    qq_musics = qq.get_music_list_infos(id)
    if album:
        super_download_musics(qq_musics, output)
    else:
        download_musics(qq_musics, output)
    if lyric:
        for music in qq_musics:
            lrc = music.lrc_url
            if lrc:
                w_lrc(output, music.name, lrc)
            else:
                print("没有歌词!")
    pass


def get_parse_id(song_id):
    # Parse the url
    if song_id.startswith('http'):
        # Not allow fragments, we just need to parse the query string
        return parse_qs(urlparse(song_id, allow_fragments=False).query)['id'][0]
    return song_id


def test_music_flac(name):
    baidu = BaiduCloud()
    baidu.get_flac_info(name)
    pass


def download_flac(name,output,lyric):
    baidu = BaiduCloud()
    music_info = baidu.get_flac_url_and_info(name)
    download_url = music_info.download_url
    song_file_name = '{}.flac'.format(music_info.name)
    switcher_song = {
        1: song_file_name,
        2: '{} - {}.flac'.format(music_info.author, music_info.name),
        3: '{} - {}.flac'.format(music_info.name, music_info.author)
    }
    song_file_name = switcher_song.get(config.SONG_NAME_TYPE, song_file_name)
    download_from_url(download_url,output+song_file_name)
    if lyric:
        lrc_url=baidu.get_lrc()
        download_from_url(lrc_url,output+name+'.lrc')
    pass


def get_xia_music_list_id(list, output, lyric, album):
    # todo:这里用正则似乎更好
    if 'collect' in list:
        id = list.split('?')[0].split('/')[-1]
    else:
        id = list
    download_xiami_playlist_songs(id, output, lyric, album)


def get_qq_music_list_id(list, output, lyric, album):
    if 'taoge' in list:
        id = list.split('=')[-1]
    else:
        id = list
    download_qq_playlist_songs(id, output, lyric, album)


def download_list(list, platform, output, lyric, album):
    if platform == 'xiami':
        get_xia_music_list_id(list, output, lyric, album)
    elif platform == 'netease':
        download_netease_playlist_songs(get_parse_id(list),output,lyric,album)
    elif platform == 'qq':
        get_qq_music_list_id(list, output, lyric, album)


def download_hot_list(platform, output, lyric, album):
    if platform == 'netease':
        download_netease_playlist_songs(netease_dict['hot'], output, lyric, album)
    elif platform == 'qq':
        download_qq_hot_songs(qq_dict['hot'], output, lyric, album)
    elif platform == 'xiami':
        download_xiami_hot_songs(xiami_dict['hot'], output, lyric, album)


def download_soar_list(platform, output, lyric, album):
    if platform == 'netease':
        download_netease_playlist_songs(netease_dict['soar'], output, lyric, album)
    elif platform == 'qq':
        download_qq_playlist_songs(qq_dict['soar'], output, lyric, album)


def download_origin_list(platform, output, lyric, album):
    if platform == 'netease':
        download_netease_playlist_songs(netease_dict['origin'], output, lyric, album)
    elif platform == 'xiami':
        download_xiami_hot_songs(xiami_dict['origin'], output, lyric, album)


def download_new_list(platform, output, lyric, album):
    if platform == 'netease':
        download_netease_playlist_songs(netease_dict['new'], output, lyric, album)
    elif platform == 'qq':
        download_qq_hot_songs(qq_dict['new'], output, lyric, album)


def main():
    music_platform = ['netease', 'qq', '1ting', 'xiami', 'kugou']
    parse = argparse.ArgumentParser(description=desc)
    parseGroup = parse.add_argument_group()
    parseGroup.add_argument("-s", "--search", action="store_true", help="search mode")
    parseGroup.add_argument("-d", "--download", action="store_true", help="download mode")
    parse.add_argument("-v", "--version", action="store_true", help="print product version")
    parse.add_argument("-tfc", "--testflac", action="store_true", help="append have flac music")
    parse.add_argument("-dfc", "--downloadflac", action="store_true", help="download flac music")
    parse.add_argument("-a", "--album", action="store_true",help="include music album info")
    parse.add_argument("-l", "--lyric", action="store_true", help="download with lyric")
    parse.add_argument("-hot", action="store_true", help="download hot music list from netease qq xiami")
    parse.add_argument("-soar", action="store_true", help="download soar music list from netease qq")
    parse.add_argument("-origin", action="store_true", help="download origin music list from netease xiami")
    parse.add_argument("-new", action="store_true", help="download new music list from netease qq")
    parse.add_argument("-uk", action="store_true", help="download uk rank from netease")
    parse.add_argument("-billboard", action="store_true", help="download Billboard rank from netease")
    parse.add_argument("-beatport", action="store_true", help="download Beatport rank from netease")
    parse.add_argument("-hito", action="store_true", help="download hito rank from netease")
    parse.add_argument("-hits", action="store_true", help="download hits rank from netease")
    parse.add_argument("-oricon", action="store_true", help="download oricon rank from netease")
    parse.add_argument("-n", "--name", type=str, help="input music name")
    parse.add_argument("-i", "--index", type=int, default=0, help="index for download music")
    parse.add_argument("-p", "--platform", type=str, choices=music_platform, default="netease",
                       help="platform you want to download include:qq,1ting,xiammi,kugou")
    parse.add_argument("-o", "--output", type=str, help="path you music")
    parse.add_argument("-t", "--list", type=str, help="netease cloud music list")
    parse.add_argument("-g", "--page", type=int, default=1, help="the page you want to change")
    args = parse.parse_args()
    name = args.name
    platform = args.platform
    offset = args.page
    index = args.index
    if args.output:
        output = args.output
    else:
        output = config.DOWNLOAD_DIR
    if args.version:
        print(version_info)
    if args.search:
        print("search\tMusicName:" + args.name + "\tPlatform:" + args.platform)
        search_or_download(name, offset, platform)
    elif args.download:
        search_or_download(name, offset, platform, False, index - 1, output, args.lyric, args.album)
    elif args.list:
        download_list(args.list, platform, output, args.lyric, args.album)
    elif args.hot:
        print("热歌下载启动：")
        download_hot_list(platform, output, args.lyric, args.album)
    elif args.soar:
        print("飙升音乐下载:")
        download_soar_list(platform, output, args.lyric, args.album)
    elif args.origin:
        print("原创榜下载启动:")
        download_origin_list(platform, output, args.lyric, args.album)
    elif args.new:
        print("新歌榜下载:")
        download_new_list(platform, output, args.lyric, args.album)
    elif args.uk:
        print("uk榜下载：")
        download_netease_playlist_songs(netease_dict['uk'], output, args.lyric, args.album)
    elif args.billboard:
        print("Billboard榜下载:")
        download_netease_playlist_songs(netease_dict['Billboard'], output, args.lyric, args.album)
    elif args.beatport:
        print("Beatport榜下载:")
        download_netease_playlist_songs(netease_dict['Beatport'], output, args.lyric, args.album)
    elif args.hito:
        print("台湾Hito排行榜:")
        download_netease_playlist_songs(netease_dict['Hito'], output, args.lyric, args.album)
    elif args.hits:
        print("法国 NRJ Vos Hits 周榜:")
        download_netease_playlist_songs(netease_dict['hits'], output, args.lyric, args.album)
    elif args.oricon:
        print("日本Oricon周榜:")
        download_netease_playlist_songs(netease_dict['Oricon'], output, args.lyric, args.album)
    elif args.testflac:
        test_music_flac(name)
    elif args.downloadflac:
        download_flac(name, output, args.lyric)


if __name__ == "__main__":
    main()
