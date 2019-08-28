from glob import glob
from src import wangyiyun, qqmusic, quanmin
import re, os, sys, getopt


def usage():
    """
    Usage:      get-more [-phvu] [Options] <URL>

    Options:
                -p,--path   Define path or default path will be used
                -h,--help   Display help information.
                -v,--version    Display version number.
                -u,--update     To update

    Example:
                get-more -p D:/file http://kg.qq.com/node/personal?uid=63999c86262c308d30
                get-more -p D:/file0 http://node.kg.qq.com/play?s=cwaiOwc4ajtBtcnI&g_f=personal
                get-more -p D:/file1 http://node.kg.qq.com/personal?uid=639d9a80212f32823c&g_f=personal
                get-more -p D:/file2 https://music.163.com/#/song?id=350909
                get-more -p D:/file3 https://music.163.com/#/artist?id=6731
                get-more -p D:/file4 https://y.qq.com/n/yqq/song/002hXDfk0LX9KO.html
                get-more https://y.qq.com/n/yqq/singer/001BHDR33FZVZ0.html?tab=song
                get-more https://www.bilibili.com/video/av20989089
                get-more -h
                get-more -v
    """


def help():
    """
    Input 'get-more' to get usage
    Input 'get-more -h' or 'get-more --help' to get help
    Input 'get-more -v' or 'get-more --version' to get version
    Input 'get-more -u' or 'get-more --update' to update
    Input 'get-more -p [PATH] [URL]' to download sth from web to path
    Input 'get-more [URL]' to download sth from web to 'C:/from_get-tool',which is a default path

    >---< If you found bugs, please send E-mail to graycat0918@gmail.com >---< Like you >---<
    """


def version():
    """
    Version:        get-tool-181014
    Designer:       duruyao
    E-mail:         graycat0918@gmail.com
    Supported Web： WangYiyunMusic  QQMusic  QuanMinMusic...

    >---< More functions will be provided >---< Stay waiting >---<
    """


def update():
    """
    This is the lastest version!
    """


# no-go function
def getpath(order):
    part = '(.+?) '
    path = re.compile(part).findall(order)
    if len(path) != 0:
        path = path[0]
        return path
    else:
        return 0


# no-go function
def geturl(order):
    part = ' (.+)'
    url = re.compile(part).findall(order)
    if len(url) != 0:
        url = url[0]
        while ' ' in url:
            url = re.compile(part).findall(url)[0]
        return url
    else:
        return 0


def judgeorigin(url):
    k0 = 'kg.qq.com'
    k1 = 'uid'
    k2 = 'play?s='
    w0 = 'music.163.com'
    w1 = 'artist?id'
    w2 = 'song?id'
    q0 = 'y.qq.com'
    q1 = 'singer'
    q2 = 'song'
    if k0 in url and k1 in url:
        flag = 'quanmin-allmusic'
    elif k0 in url and k2 in url:
        flag = 'quanmin-singlemusic'
    elif w0 in url and w1 in url:
        flag = 'wangyiyun-allmusic'
    elif w0 in url and w2 in url:
        flag = 'wangyiyun-siglemusic'
    elif q0 in url and q1 in url:
        flag = 'qqmusic-allmusic'
    elif q0 in url and q2 in url:
        flag = 'qqmusic-singlemusic'
    else:
        flag = 'you-get'
    return flag


def download(url, path):
    flag = judgeorigin(url)
    if flag == 'quanmin-allmusic':
        QuanMin.getallmusic(url, path)
    elif flag == 'quanmin-singlemusic':
        QuanMin.getsinglemusic(url, path)
    elif flag == 'wangyiyun-allmusic':
        WangYiYun.getallmusic(url, path)
    elif flag == 'wangyiyun-siglemusic':
        WangYiYun.getsinglemusic(url, path)
    elif flag == 'qqmusic-allmusic':
        QQMusic.getallmusic(url, path)
    elif flag == 'qqmusic-singlemusic':
        QQMusic.getsinglemusic(url, path)
    else:
        get_video = 'you-get ' + '-o ' + path + ' ' + url
        os.system(get_video)
        for file in glob(os.path.join(path, '*.xml')):
            os.remove(file)
        print('Sth is downloaded in ' + path + ' successfully')


def do_main():
    path, url = ['C:/from_get-tool', '']
    opts, args = ['', '']
    if not len(sys.argv[1:]):
        print(usage.__doc__)
        sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:hvu", ["path", "help", "version", "update"])
    except getopt.GetoptError as e:
        print(e)
        print(usage.__doc__)
        sys.exit()

    for opt_name, opt_value in opts:
        if opt_name in ('-p', '--path'):
            path = opt_value
        elif opt_name in ('-h', '--help'):
            print(help.__doc__)
        elif opt_name in ('-v', '--version'):
            print(version.__doc__)
        elif opt_name in ('-u', '--update'):
            print(update.__doc__)
    for opt_value in args:
        url = opt_value
    # if len(opts) == 0 and len(args) == 0:
    #     print(usage.__doc__)
    #     sys.exit()
    # else:
    #     if len(url) != 0:
    #         download(url, path)
    if len(sys.argv[1:]) and len(url):
        download(url, path)
