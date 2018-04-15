from tabulate import tabulate

def show_music(info_list):
    # print(" "+str(index) + "\t" + music_name + "\t" + authors + "\t"  + album)
    # print(" {:^4}\t{:40}\t{:20}\t{:40}".format(index,music_name,authors,album))
    print(tabulate(info_list,headers=['#','Song','Artist','Album'],tablefmt='fancy_grid'))

def show_title():
    # print("Index\tMusicName\tMusicAuthor\tMusicAlbum")
    print(" {:^4}\t{:40}\t{:20}\t{:40}".format('Index','Music_Name','Authors','Album'))

def show_out_of_bound():
    print('越界错误')
