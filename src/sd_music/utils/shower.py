
def show_music(index,music_name,authors,album=''):
    # print(" "+str(index) + "\t" + music_name + "\t" + authors + "\t"  + album)
    print(" {:^4}\t{:40}\t{:20}\t{:40}".format(index,music_name,authors,album))

def show_title():
    # print("Index\tMusicName\tMusicAuthor\tMusicAlbum")
    print(" {:^4}\t{:40}\t{:20}\t{:40}".format('Index','Music_Name','Authors','Album'))

def show_out_of_bound():
    print('越界错误')
