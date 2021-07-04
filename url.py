from __future__ import unicode_literals
import os
import json
import lz4.block
import requests
import youtube_dl
import sys
from eyed3 import id3
from urllib.request import urlopen, FancyURLopener
from urllib.parse import urlparse, parse_qs, unquote
import tkinter

from settings import settings

tag = id3.Tag()
i = sys.argv[1]

if "https://www.youtube.com/watch?" in i:
    ydl_opts = {
        'format': 'bestaudio/best',
        'forcetitle': 'true',
        'forcejson': 'true',
        'noplaylist': 'true',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(i.split("&index")[0].split("&list=")[0], download=False)
        ydl.download([i.split("&index")[0].split("&list=")[0]])
        print(info_dict["title"]+'-' +info_dict["id"]+".mp3")
        tag.parse(info_dict["title"]+'-' +info_dict["id"]+".mp3")
        title = 'default'
        if (len(info_dict["title"].split(" - ")) > 1):
            tag.title = info_dict["title"].split(" - ")[0]
            tag.artist = info_dict["title"].split(" - ")[1]
            title = info_dict["title"].split("-")[0]
        elif(len(info_dict["title"].split("-")) > 1):
            tag.title = info_dict["title"].split("-")[0]
            tag.artist = info_dict["title"].split("-")[1]
            title = info_dict["title"].split("-")[0]
        else:
            tag.title = info_dict["title"]
            title = info_dict["title"]
        
        tag.save()
        var = info_dict["title"]+'-' +info_dict["id"]+".mp3"
        os.rename(var, settings["pathMusique"] + '/ToSort/'+ title + ".mp3")