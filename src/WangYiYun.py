import urllib.request
from tqdm import tqdm
import re
import os
import requests


def getrealurl(url):
    if '#/' in url:
        part1 = '(.+)#/'
        part2 = '#/(.+)'
        return re.compile(part1).findall(url)[0] + re.compile(part2).findall(url)[0]
    else:
        return url


def gethtml(url):
    headers = {
        'Host': 'music.163.com',
        'Origin': 'https://music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        print('Request Error!')
        pass


def getsongname(songurl):
    songurl = getrealurl(songurl)
    html = gethtml(songurl)
    part0 = '<title>(.+?) - 单曲'
    part1 = '<title>(.+?) - '
    part2 = '<title>(.+?)/'
    songname = re.compile(part0).findall(html)
    if len(songname) != 0:
        songname = songname[0]
        if len(songname) > 40:
            songname = re.compile(part1).findall(html)[0]
        if '/' in songname:
            songname = re.compile(part2).findall(html)[0]
        return songname
    else:
        return '未知歌曲 - 未知歌手'


def getsongidlist(perurl):
    perurl = getrealurl(perurl)
    html = gethtml(perurl)
    part = 'song\?id=(.+?)">'
    songidlist = re.compile(part).findall(html)
    if len(songidlist) != 0:
        return songidlist
    else:
        print("can't get songidlist")
        return 0


def downmusic(songid, path):
    u1 = 'http://music.163.com./song/media/outer/url?id='
    u2 = '.mp3'
    downurl = u1 + songid + u2
    songurl = 'https://music.163.com/song?id=' + songid
    songname = getsongname(songurl)
    filename = path + '/' + songname + '.mp3'
    if not (os.path.exists(path)):
        os.makedirs(path)
    if not (os.path.exists(filename)):
        urllib.request.urlretrieve(downurl, filename=filename)


def getsinglemusic(songurl, path):
    part = 'id=(.*)'
    songid = re.compile(part).findall(songurl)[0]
    songname = getsongname(songurl)
    downmusic(songid, path)
    print(songname + '.mp3 is downloaded in ' + path + ' successfully.')


def getallmusic(perurl, path):
    songidlist = getsongidlist(perurl)
    for songid in tqdm(songidlist):
        downmusic(songid, path)
    print('all the musics are downloaded in ' + path + ' successfully.')
