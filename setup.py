# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='sdmusic',
        version='0.12',
        packages=find_packages('src'),
        package_dir = {'':'src'},


    install_requires=[
                'requests>=2.17.3',
                'pycrypto>=2.6.1',
                'mutagen>=1.38.0',
                'tqdm>=4.19.5',
                'pydub>=0.20.0',
    ],

    entry_points={
        'console_scripts': [
                        'sdmusic = sd_music.start:main',
        ]
            
    },

        license='MIT',
        author='pcdack',
        author_email='ibackud@gmail.com',
        url='https://github.com/pcdack/SDMUSIC',
        description='Search && Download Music from netease qq,1ting,kugou and xiami',
        keywords=['sdmusic', 'netease','qq','kugou', 'music', 'downloader'],
    )
