import urllib.request
import urllib.error
from tqdm import tqdm
import requests
import re
import os


def gethtml(url):
    headers = {
        'Host': 'node.kg.qq.com',
        'Origin': 'http://node.kg.qq.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        print('Request Error!')
        pass


def getnum(perurl):
    html = gethtml(perurl)
    part = 'content="作品: (.+?); 粉丝'
    num = int(re.compile(part).findall(html)[0])
    return num


def getrealurl(perurl):
    string = '&g_f=personal'
    if string not in perurl:
        u0 = 'http://node.kg.qq.com/personal?uid='
        part = 'uid=(.+)'
        uid = re.compile(part).findall(perurl)[0]
        realperurl = u0 + uid + string
    else:
        realperurl = perurl
    return realperurl


def getuid(perurl):
    part = 'uid=(.*?)_f=personal'
    uid = re.compile(part).findall(perurl)[0]
    return uid


def checksongname(songname):
    part = '(.+?)/'
    while '/' in songname:
        songname = songname.replace('/','&')
    return songname


def getsinglemusic(songurl, path):
    if not (os.path.exists(path)):
        os.makedirs(path)
    html0 = gethtml(songurl)
    part0 = '"playurl":"(http.+?)",'
    downurl = re.compile(part0).findall(html0)
    flag = 1
    if len(downurl) == 0:
        part1 = 'playurl_video":"(http.+?)",'
        downurl = re.compile(part1).findall(html0)
        flag = 0
    downurl = downurl[0]
    # songname
    part2 = '<title>(.*?)- 全民K歌'
    songname = re.compile(part2).findall(html0)[0]
    songname = re.compile('-(.+)').findall(songname)[0] + ' - ' + re.compile('(.+?)-').findall(songname)[0]
    songname = checksongname(songname)
    # filename
    if flag:
        filename = path + '/' + songname + '.mp3'
    else:
        filename = path + '/' + songname + '.mp4'
    try:
        if not (os.path.exists(filename)):
            urllib.request.urlretrieve(downurl, filename=filename)
            print(songname + '.mp3 is downloaded in ' + path + ' successfully.')
        else:
            print(songname + '.mp3 had already existed in ' + path)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):  # HTTPError
            print('HTTPError: ' + e.code)
        if hasattr(e, 'reason'):  # URLErrorl
            print('URLError: ' + e.reason)


def getallmusic(perurl, path):
    u1 = 'http://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_2&g_tk=5381&outCharset=utf-8&format=jsonp&type=get_ugc&start='  # + page
    u2 = '&num=1&touin=&share_uid='  # + uid
    u3 = '_tk_openkey=982796762&_=1524370798837'
    # path
    if not os.path.exists(path):
        os.makedirs(path)
    perurl = getrealurl(perurl)
    num = getnum(perurl)
    uid = getuid(perurl)
    # 按页download，共num页
    for i in tqdm(range(1, num + 1)):
        url = u1 + str(i) + u2 + uid + u3
        req1 = urllib.request.Request(url)
        html1 = str(urllib.request.urlopen(req1).read())
        part2 = 'shareid": "(.+?)",'
        s = re.compile(part2).findall(html1)[0]
        songurl = 'http://kg.qq.com/node/play?s=' + s
        req2 = urllib.request.Request(songurl)
        html2 = str(urllib.request.urlopen(req2).read(), 'utf-8')  # 汉字解码
        part3 = 'playurl":"(http.+?)",'
        part4 = '<title>(.*?)- 全民K歌'
        downurl = re.compile(part3).findall(html2)
        flag = 0
        # MV type
        if len(downurl) == 0:
            part3_1 = 'playurl_video":"(http.+?)",'
            downurl = re.compile(part3_1).findall(html2)[0]
            flag = 1
        else:
            downurl = re.compile(part3).findall(html2)[0]
        songname = re.compile(part4).findall(html2)[0]
        songname = re.compile('-(.+)').findall(songname)[0] + ' - ' + re.compile('(.+?)-').findall(songname)[0]
        songname = checksongname(songname)
        filename = path + '/' + songname + '.mp3'
        # MV type
        if flag == 1:
            filename = path + '/' + songname + '.mp4'
        try:
            if not (os.path.exists(filename)):
                urllib.request.urlretrieve(downurl, filename=filename)
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):  # HTTPError
                print('HTTPError: ' + e.code)
                #  break
            if hasattr(e, 'reason'):  # URLError
                print('URLError: ' + e.reason)
                #  break
    print('all the musics are downloaded in ' + path + ' successfully.')
