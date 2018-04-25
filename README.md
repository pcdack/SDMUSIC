
# SDMusic多平台音乐搜索下载工具

```shell
 ______     _____     __    __     __  __     ______     __     ______    
/\  ___\   /\  __-.  /\ "-./  \   /\ \/\ \   /\  ___\   /\ \   /\  ___\   
\ \___  \  \ \ \/\ \ \ \ \-./\ \  \ \ \_\ \  \ \___  \  \ \ \  \ \ \____  
 \/\_____\  \ \____-  \ \_\ \ \_\  \ \_____\  \/\_____\  \ \_\  \ \_____\ 
  \/_____/   \/____/   \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_____/

```



Search && Download Music Cli
version 0.13

本软件只用来交流测试与学习。
支持的搜索和下载平台：网易，QQ，酷狗，虾米，一听
支持的系统：理论上支持所有的系统，已测试系统Linux(Arch,Ubuntu,Mac(网友测试，十分感谢))

>代码写的如屎一般，还请各位提提写法上的issue。谢谢。根据文件下载音乐将在下个commit中实现

> 4-25
使用qq音乐无损平台（感谢[BigUncle](https://github.com/BigUncle)提供的接口），代替原本的百度音乐。注意现在无损接口是尽可能下载相关的音乐。无法使用\-l参数

> 4-17
修复qq音乐平台无法下载的BUG

> 4-15
修改了部分BUG，美化了结果输出。非常感谢[raawaa](https://github.com/raawaa)。

> 3-5
 量下载UK榜,美国Billboard周榜,Beatport全球电子舞曲榜,法国 NRJ Vos Hits 周榜,日本Oricon周榜,台湾Hito排行榜

> 3-1
新增飙升榜（网易云，QQ）音乐下载，新增原创榜下载（网易云，虾米音乐），热歌榜新增虾米音乐

> 2-28
新增网易云和QQ音乐热歌榜下载,指定参数\-hot加平台就可以了,修复\/的BUG

> 2-27
 增QQ音乐歌单下载，需要指定\-p qq。注意qq音乐批量下载中需要将`https://y.qq.com/w/taoge.html?ADTAG=newyqq.taoge&id=3710267240`改为`https://y.qq.com/w/taoge.html?ADTAG=newyqq.taoge\&id=3710267240`否则无法正常工作。


> 新增加虾米歌单下载，注意歌单下载默认是网易云，可以通过\-p xiami来下载虾米音乐，修复高清测试空格出错的情况.

## 功能清单
- [x] 搜索
- [x] 下载
- [x] 歌词
- [x] 专辑图片下载与嵌入(*在下载时指定\-a参数,实现此功能依赖你电脑的ffmpeg*)
- [x] 批量下载(*使用\-t参数，后跟playlist的URL，暂时只支持网易云,虾米，支持批量歌词下载，批量专辑图嵌入*)
- [x] 高清音乐源(*使用\-tfc(test flac)参数来测试音乐是否有flac无损格式的，通过\-dfc(download flac)来下载flac格式的音乐，flac格式自带信息嵌入，所以不需要也不容许使用\-a，但可以使用\-l*)
- [x] 增加配置文件，给用户更多自定义功能
- [x] 批量下载hot(网易云热歌榜，QQ音乐热歌榜,虾米音乐榜)
- [x] 批量下载soar(网易云飙升榜,QQ飙升榜)
- [x] 批量下载origin(网易云原创,虾米原创)
- [x] 批量下载new(网易云新歌榜，QQ音乐新歌榜)
- [x] 批量下载UK榜,美国Billboard周榜,Beatport全球电子舞曲榜,法国 NRJ Vos Hits 周榜,日本Oricon周榜,台湾Hito排行榜
- [ ] 根据文件下载音乐

## 配置
配置文件的位置`~/.sdmusic/sdmusic.config`
### 可配置的项
**文件名的命名格式**
1. 歌曲名
2. 歌手 - 歌曲名
3. 歌曲名 - 歌手

例如:我想使用第二种命名方式,那么我们只需要将配置文件中
```shell
 song.name_type = 2
```
**歌曲默认下载路径**
例如修改到`/home/{username}/Music/test/`目录下:
> 注意：路径要写全，否则可能报错 

```shell
 download.dir = /home/{username}/Music/test/
```



## 安装

### 方法一

```shell
pip3 install sdmusic
```

### 方法二

```shell
git clone git@github.com:pcdack/SDMUSIC.git
cd SDMUSIC/
python3 setup.py install
```

## 使用



### 搜索命令

```shell
sdmusic -n "体面" -s
```
**可选参数**
\-p[platform]:可以指定搜索平台{netease(网易:默认)，qq,xiami(虾米),kugou(酷狗),1ting(一听)}
例子
```shell
sdmusic -n "体面" -p qq -s
```
\-g[page]:指定搜索的页面为第几页默认为第一页，如果第一页没有找到相关的歌曲，可以指定移动到第二页
```shell
sdmusic -n "体面" -p qq -g 1 -s
```

\-o[output]:指定输出路径(*只有在指定为下载是有效*)

\-l[lyric]:下载歌词(*只有在指定为下载是有效,不支持一听平台*)

\-a[album]:下载并嵌入专辑图片,专辑名字，作者名字等信息，全平台适用





![](./gif/search.gif)

### 下载命令

> 可选参数与搜索命令一样

很简单只要把上面的s参数改为d，然后用\-i在去指定你要下载那一条音乐

例如
```shell
sdmusic -n "体面" -p qq -s
```
在命令行的结果为
```shell
Index   MusicName       MusicAuthor
1       体面    于文文
2       体面    艾辰
3       体面    简弘亦
4       体面    罗之豪
5       体面    胖胖胖
6       体面    阿细
7       体面    妖蝠sama
8       体面    冯允澈
9       体面    阿祥
10      体面    简弘亦
```
我们如果想下载第一个音乐，那么
> 技巧使用键盘的上键更改即可

```shell
sdmusic -n "体面" -p qq -d -i 1
```
回车就可下载
![](./gif/download.gif)

#### 批量下载
**歌单下载**

```shell
sdmusic -l -a -t http://music.163.com/#/playlist?id=932596614
```
或
```shell
sdmusic -l -a -t 932596614
```
批量下载虾米歌单：
```shell
sdmusic -p xiami -t http://www.xiami.com/collect/281354699?spm=a1z1s.2943601.6856193.2.LkPhvN
```
批量下载QQ音乐歌单:
> 注意`&`符号前一定要加\\否则会报错

```shell
sdmusic -p qq -t https://y.qq.com/w/taoge.html?ADTAG=newyqq.taoge\&id=3710267240 
```
直接指定ID
```shell
sdmusic -p qq -t 3710267240
```

**下载热歌**
网易云
```shell
sdmusic -hot
```
QQ音乐
```shell
sdmusic -hot -p qq
```
虾米音乐
```shell
sdmusic -hot -p xiami
```
**下载飙升榜**
网易云
```shell
sdmusic -soar
```
QQ音乐
```shell
sdmusic -soar -p qq
```
**下载原创**
网易云
```shell
sdmusic -origin
```
虾米
```shell
sdmusic -origin -p xiami
```

**下载其他榜单**
这里以UK榜为例
```shell
sdmusic -uk
```

*其他榜*

* 日本Oricon周榜:oricon
* 美国Billboard周榜:billboard
* Beatport全球电子舞曲榜:beatport
* 法国 NRJ Vos Hits 周榜:hits
* 台湾Hito排行榜:hito



* \-l:批量下载歌词
* \-a:批量将专辑图嵌入音乐

#### 无损音乐测试与下载
 * 测试是否存在无损音乐

```shell
sdmusic -tfc -n "黄色大门"
```

* 下载无损音乐（先测试是否存在）
```shell
sdmusic -dfc -n "黄色大门"
```
> 自带专辑图片和专辑信息，所以emmmmm\-a属性没什么软用。当然\-l(下载歌词)依然可用


Enjoy!
