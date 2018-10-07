from __future__ import unicode_literals
import os
import json
import lz4.block
import requests
import youtube_dl
from urllib.request import urlopen, FancyURLopener
from urllib.parse import urlparse, parse_qs, unquote

from settings import settings

f = open(settings["path"] + "/recovery.jsonlz4", "rb")
magic = f.read(8)
jdata = json.loads(lz4.block.decompress(f.read()).decode("utf-8"))
f.close()
URLS = []
for win in jdata.get("windows"):
    for tab in win.get("tabs"):
        i = tab.get("index") - 1
        urls = tab.get("entries")[i].get("url")
        if "www.youtube.com" in urls:
            list.append(URLS,urls)

for i in URLS:
    video_id = parse_qs(urlparse(i).query)['v'][0]

    url_data = urlopen('http://www.youtube.com/get_video_info?&video;_id=' + video_id).read()
    url_info = parse_qs(unquote(url_data.decode('utf-8')))
    ydl_opts = {
        'format': 'bestaudio/best',
        'forcetitle': 'true',
        'forcejson': 'true',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(i, download=False)
        print(info_dict["title"])
        title = input("Titre de la musique: ")
        ydl.download([i])
        dir = os.listdir(settings["pathMusique"])
        for i in range(0,len(dir)):
            print(str(i) + " - " + dir[i])
        dirFinal = dir[int(input("Dossier final:"))]
        os.rename(info_dict["title"]+'-' +info_dict["id"]+".mp3",settings["pathMusique"] + '/'+ dirFinal +'/' + title +".mp3")
