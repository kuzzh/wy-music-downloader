# Filename: wyMusicDownloader.py
# -*- coding: UTF-8 -*-
# Author: sarlanori
# Created Date: 2015-02-21
# Modified Date: 2015-02-25

import urllib2
import urllib
import re
import json
import sys
import os.path

reload(sys)
sys.setdefaultencoding("utf-8")

class mp3Item:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.artist = ''
        self.mp3url = ''

def getSongListPageSource(url):
    return urllib2.urlopen(url.replace("#/", "")).read()

def getAllMusicIds(pageSource):
    matches = re.finditer(r'<a href=\"/song\?id=(\d+)\" title=\".*\">(.*)</a>', pageSource)
    musicIdList = []
    for m in matches:
        musicIdList.append(m.group(1))

    return musicIdList

def getSongListName(pageSource):
    match = re.search(r'<h2 class=\"f-ff2 f-brk\">(.*)</h2>', pageSource)
    return match.group(1)

def getAllMp3Items(musicIdList):
    mp3ItemList = []
    for musicId in musicIdList:
        resp = urllib2.urlopen('http://music.163.com/api/song/detail/?id=' + musicId + '&ids=%5B' + musicId + '%5D')
        jsonStr = resp.read()
        obj = json.loads(jsonStr)
        item = mp3Item()
        item.id = obj['songs'][0]['id']
        item.name = obj['songs'][0]['name']
        item.artist = obj['songs'][0]['artists'][0]['name']
        item.mp3url = obj['songs'][0]['mp3Url']
        mp3ItemList.append(item)
    return mp3ItemList

def download_music_list(url, save_path):
    print 'Retrieve song list page source ...'
    pageSource = getSongListPageSource(url)
    print 'Retrieve song list name ...'
    songListName = getSongListName(pageSource)
    print 'Retrieve music ids ...'
    musicIdList = getAllMusicIds(pageSource)
    print 'Retrieve music mp3 urls ...'
    mp3ItemList = getAllMp3Items(musicIdList)

    if (save_path == None):
        save_path = songListName

    if (os.path.exists(save_path) == False):
        os.mkdir(save_path)

    i = 1
    for mp3Item in mp3ItemList:
        print 'Downloading(' + str(i) + '/' + str(len(mp3ItemList)) + ') ' + mp3Item.name
        urllib.urlretrieve(mp3Item.mp3url, os.path.join(save_path, mp3Item.name.replace("/", "\\") + '-' + mp3Item.artist + '.mp3'))
        i += 1

if (len(sys.argv) < 2):
    print 'wyMusicDownloader.py: illegal option -- - '
    print 'usage: python wyMusicDownloader.py [song list url] [optional][local save path]'
    exit()

url = sys.argv[1]
save_path = None
if (len(sys.argv) >= 3):
    save_path = sys.argv[2]

download_music_list(url, save_path)

print 'Download completed.'

