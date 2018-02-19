#!/usr/bin/env python3
# coding=utf-8
import os

from configparser import ConfigParser

# Config Key

_CONFIG_KEY_SONG_NAME_TYPE = 'song.name_type'
_CONFIG_KEY_DOWNLOAD_DIR = 'download.dir'

# Base Path
_CONFIG_MAIN_PATH = os.path.join(os.path.expanduser('~'),'.sdmusic')
_CONFIG_FILE_PATH = os.path.join(_CONFIG_MAIN_PATH,'sdmusic.config')
_CONFIG_DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'),'Music')

# Global config value
DOWNLOAD_DIR = '~/Music'
SONG_NAME_TYPE = 1

def load_config():
    if not os.path.exists(_CONFIG_FILE_PATH):
        init_config_file()

    cfg = ConfigParser()
    cfg.read(_CONFIG_FILE_PATH)

    global DOWNLOAD_DIR
    global SONG_NAME_TYPE

    DOWNLOAD_DIR = cfg.get('settings', _CONFIG_KEY_DOWNLOAD_DIR)
    SONG_NAME_TYPE = cfg.getint('settings', _CONFIG_KEY_SONG_NAME_TYPE)


def init_config_file():
    default_config = '''\
    [settings]

    #--------------------------------------
    # Song download directory音乐下载目录
    #--------------------------------------
    {key_dir} = {value_dir}

    #--------------------------------------
    # The way music is named:
    # 音乐命名的方式:
    # 1: song_name.mp3
    # 2: artist_name - song_name.mp3
    # 3: song_name - artist_name.mp3
    #--------------------------------------
    {key_name_type} = 1
    '''.format(key_dir=_CONFIG_KEY_DOWNLOAD_DIR,
               value_dir=_CONFIG_DOWNLOAD_PATH,
               key_name_type=_CONFIG_KEY_SONG_NAME_TYPE)

    if not os.path.exists(_CONFIG_MAIN_PATH):
        os.makedirs(_CONFIG_MAIN_PATH)
    f = open(_CONFIG_FILE_PATH, 'w')
    f.write(default_config)
    f.close()