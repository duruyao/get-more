'''
persingleurl = 'https://y.qq.com/n/yqq/singer/001BHDR33FZVZ0.html?tab=song'
path = 'D:/毛不易'
QQMusic.getallmusic(persingleurl, path)
order = 'get-tool D:/downloads http://kg.qq.com/node/personal?uid=63999c86262c308d30'
order0 = 'get-tool D:/download0 http://node.kg.qq.com/play?s=cwaiOwc4ajtBtcnI&g_f=personal'
order1 = 'get-tool D:/downloads1 http://node.kg.qq.com/personal?uid=639d9a80212f32823c&g_f=personal'
order2 = 'get-tool D:/downloads2 https://music.163.com/#/song?id=350909'
order3 = 'get-tool D:/downloads3 https://music.163.com/#/artist?id=6731'
order4 = 'get-tool D:/downloads4 https://y.qq.com/n/yqq/song/002hXDfk0LX9KO.html'
order5 = 'get-tool D:/毛不易 https://y.qq.com/n/yqq/singer/001BHDR33FZVZ0.html?tab=song'
order6 = 'get-tool D:/downloads6 https://www.bilibili.com/video/av20989089'
'''
def checksongname(songname):
    part = '(.+?)/'
    while '/' in songname:
        songname = songname.replace('/','&')
    return songname

songname = 'GUN/Papillon(Live) - 王子异/蔡徐坤/卜凡/Justin - 滚滚没有骂人'
songname=checksongname(songname)
print(songname)