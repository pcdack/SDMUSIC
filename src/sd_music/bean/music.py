
# 音乐的名字，作者名字,专辑名字，专辑图片URL
class Music(object):

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,id):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self,authors):
        self.__author = authors

    @property
    def album_name(self):
        return self.__album_name

    @album_name.setter
    def album_name(self,name):
        self.__album_name = name

    @property
    def album_pic_url(self):
        return self.__album_pic_url

    @album_pic_url.setter
    def album_pic_url(self,url):
        self.__album_pic_url = url

    @property
    def download_url(self):
        return self.__download_url

    @download_url.setter
    def download_url(self,url):
        self.__download_url = url

    @property
    def download_index(self):
        return self.__download_index

    @download_index.setter
    def download_index(self,index):
        self.__download_index = index

    @property
    def lrc_url(self):
        return self.__lrc_url

    @lrc_url.setter
    def lrc_url(self,url):
        self.__lrc_url = url