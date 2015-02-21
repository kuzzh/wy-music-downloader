# -*- coding: UTF-8 -*-

import urllib2
import urllib
import re
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def getAllMusicIds(url):
    resp = urllib2.urlopen(url)
    htmlStr = resp.read()
    matches = re.finditer(r'<a href=\"/song\?id=(\d+)\" title=\".*\">(.*)</a>', htmlStr)
    musicIdList = []
    for m in matches:
        musicIdList.append(m.group(1))
    return musicIdList

def getAllMp3Urls(musicIdList):
    mp3UrlDict = {}
    for musicId in musicIdList:
        resp = urllib2.urlopen('http://music.163.com/api/song/detail/?id=' + musicId + '&ids=%5B' + musicId + '%5D')
        jsonStr = resp.read()
        obj = json.loads(jsonStr)
        print obj['songs'][0]['name'] + ": " + obj['songs'][0]['mp3Url']
        mp3UrlDict[obj['songs'][0]['name']] = obj['songs'][0]['mp3Url']
    return mp3UrlDict

def load_config():
    f = file('MusicUrlList.json')
    config = json.load(f)
    f.close
    return config

config = load_config()
for c in config:
    print 'Downloading ' + c
    urllib.urlretrieve(config[c], 'mp3/' + c + '.mp3')
#musicIdList = getAllMusicIds('http://music.163.com/playlist?id=6028012')
#mp3UrlDict = getAllMp3Urls(musicIdList)

#f = open('MusicUrlList.json', 'w')
#json.dump(mp3UrlDict, f)
#f.close()

#print 'Download complete.'

