import requests
import urllib.request
import urllib.error
from tqdm import tqdm
import math
import re
import os


def gethtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        print('Request Error!')
        pass


def getsongname(html):
    part1 = 'songtitle":"(.+?)"'
    part2 = 'singername":"(.+?)"'
    song = re.compile(part1).findall(html)
    singer = re.compile(part2).findall(html)
    if len(song) != 0 and len(singer) != 0:
        songname = song[0] + ' - ' + singer[0]
        while '/' in songname:
            songname = re.compile('/(.+?)').findall(songname)[0]
        return songname
    else:
        return '未知歌曲 - 未知歌手'


def checksongname(songname):
    part = '(.+?)/'
    while '/' in songname:
        songname = songname.replace('/', '&')
    return songname


def getdownurl(songmid):
    u1 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=1400579671&jsonpCallback=MusicJsonCallback1725281637681917&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback1725281637681917&uin=0&songmid=%s&filename=%s&guid=7286222600'
    u2 = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=7286222600&uin=0&fromtag=66'
    filename = 'C400' + songmid + '.m4a'
    url = u1 % (songmid, filename)
    html = gethtml(url)
    part = 'vkey":"(.+?)"}'
    vkey = re.compile(part).findall(html)
    if len(vkey) != 0:
        vkey = vkey[0]
        downurl = u2 % (filename, vkey)
        return downurl
    else:
        #  print('vkey = NULL')
        return ''


def getsongmidlist(persingleurl):
    u1 = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid=%s&order=listen&begin=%d&num=30&songstatus=1'
    part0 = "singermid : '(.+?)'"
    part1 = 'data_statistic__number">(.+?)<'
    part2 = 'songmid":"(.+?)",'
    html = gethtml(persingleurl)
    singermid = re.compile(part0).findall(html)[0]
    num = re.compile(part1).findall(html)[0]
    pages = int(math.ceil(int(num) / 30))
    #  begin = -1
    songmidlist = []
    for begin in range(1, pages + 1):
        begin = (begin - 1) * 30
        url = u1 % (singermid, begin)
        html = gethtml(url)
        newlist = re.compile(part2).findall(html)
        songmidlist.extend(newlist)
    return songmidlist


def getsinglemusic(songurl, path):
    part = 'songmid=(.+?)#'
    html = gethtml(songurl)
    songmid = re.compile(part).findall(html)[0]
    downurl = getdownurl(songmid)
    songname = getsongname(html)
    songname = checksongname(songname)
    filename = path + '/' + songname + '.mp3'
    if not (os.path.exists(path)):
        os.makedirs(path)
    if not (os.path.exists(filename)):
        urllib.request.urlretrieve(downurl, filename=filename)
        print(songname + '.mp3 is downloaded in ' + path + ' successfully.')
    else:
        print(songname + '.mp3 had already existed in ' + path)

    return 0


def getallmusic(persingleurl, path):
    if not (os.path.exists(path)):
        os.makedirs(path)
    songmidlist = getsongmidlist(persingleurl)
    for songmid in tqdm(songmidlist):
        songurl = 'https://y.qq.com/n/yqq/song/%s.html' % (songmid)
        html = gethtml(songurl)
        songname = getsongname(html)
        songname = checksongname(songname)
        downurl = getdownurl(songmid)
        filename = path + '/' + songname + '.mp3'
        if not (os.path.exists(filename)) and len(downurl) != 0:
            urllib.request.urlretrieve(downurl, filename=filename)
    print('all the musics are downloaded in ' + path + ' successfully.')

    return 0
