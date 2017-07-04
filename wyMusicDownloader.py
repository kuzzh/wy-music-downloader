#! coding:utf-8

# Filename: wyMusicDownloader.py
# Author: sarlanori
# Created Date: 2015-02-21
# Modified Date: 2015-02-25

# pylint: disable=C0111,C0301,C0103,W0512


import urllib2
import urllib
import re
import json
import sys
import os.path
import getopt

import encryptutil

reload(sys)
sys.setdefaultencoding("utf-8")


def get_song_list_page_source(page_url):
    return urllib2.urlopen(page_url.replace("#/", "")).read()


def get_song_list_ids(page_source):
    matches = re.finditer(
        r'<a href=\"/song\?id=(\d+)\">(.*?)</a>', page_source)
    music_id_list = []
    for match in matches:
        music_id_list.append(match.group(1))

    return music_id_list


def get_song_list_name(page_source):
    match = re.search(r'<h2 class=\"f-ff2 f-brk\">(.*)</h2>', page_source)
    return match.group(1).decode('utf-8')


def get_song_detail_list(song_id_list, bitrate):
    song_detail_list = []
    for song_id in song_id_list:
        resp = urllib2.urlopen('http://music.163.com/api/song/detail/?id=' + song_id + '&ids=%5B' + song_id + '%5D')
        json_str = resp.read()
        obj = json.loads(json_str)
        item = {
            'id': obj['songs'][0]['id'],
            'name': obj['songs'][0]['name'].decode('utf-8'),
            'artist': obj['songs'][0]['artists'][0]['name'].decode('utf-8'),
        }
        song_detail_list.append(item)

    song_detail_list = get_mp3_url_list(song_detail_list, bitrate)

    return song_detail_list

def get_mp3_url_list(song_detail_list, bitrate):
    url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    song_id_list = []
    for detail in song_detail_list:
        song_id_list.append(detail['id'])
    data = {
        'ids': song_id_list,
        # br 代表比特率(Bitrate)，常用取值：192000、128000、320000、990000...值越大代表音质越好，文件也越大
        'br': bitrate
    }
    data = json.dumps(data)
    json_result = encryptutil.encrypt_request(url, data)
    obj = json.loads(json_result)
    for item in obj['data']:
        detail = next(x for x in song_detail_list if x['id'] == item['id'])
        detail['mp3url'] = item['url']
        detail['size'] = item['size']
        detail['bitrate'] = item['br']
    return song_detail_list

def start(song_list_url, bitrate, local_save_path):
    print '正在下载歌单源码...'.decode('utf-8')
    page_source = get_song_list_page_source(song_list_url)
    print '正在获取歌单名称...'.decode('utf-8')
    song_list_name = get_song_list_name(page_source)

    if local_save_path is None:
        local_save_path = song_list_name

    song_detail_list = None

    detail_list_save_path = os.path.join(local_save_path, song_list_name + ".json")
    if os.path.exists(detail_list_save_path):
        song_detail_list = json.loads(detail_list_save_path)
    else:
        print '正在获取歌曲 ids...'.decode('utf-8')
        song_id_list = get_song_list_ids(page_source)
        print '正在获取歌曲详细信息...'.decode('utf-8')
        song_detail_list = get_song_detail_list(song_id_list, bitrate)

    if os.path.exists(local_save_path) is False:
        os.mkdir(local_save_path)

    i = 1
    for song_detail in song_detail_list:
        file_path = os.path.join(local_save_path, song_detail['name'].replace("/", "\\") + '-' + song_detail['artist'] + '.mp3')
        print '正在下载(%d/%d) %s' % (i, len(song_detail_list), song_detail['name'])
        i += 1
        if os.path.exists(file_path):
            continue
        urllib.urlretrieve(song_detail['mp3url'], file_path)

    with open(detail_list_save_path, "w") as handle:
        handle.write(json.dumps(song_detail_list))

def usage():
    print '使用方法：python wyMusicDownloader.py [-o local/save/path](可选) [-b bitrate](可选) [song list url]'.decode('utf-8')

if __name__ == '__main__':
    # sys.argv 第一个参数为执行脚本的名称
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:b:h', ['output=', 'bitrate=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit()

    if len(args) < 1:
        usage()
        sys.exit()

    _song_list_url = args[0]
    output = None
    _bitrate = 192000

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-o', '--output'):
            output = a
        elif o in ('-b', '--bitrate'):
            _bitrate = a

    start(_song_list_url, _bitrate, output)

    print '下载完成！'
