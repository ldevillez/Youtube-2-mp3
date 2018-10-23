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

# On regarde dans quel mode on est
if(len(sys.argv) < 2):
    tag = id3.Tag()
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
                tag.parse(info_dict["title"]+'-' +info_dict["id"]+".mp3")
                title = 'default'
                if (len(info_dict["title"].split(" - ")) > 1):
                    tag.title = info_dict["title"].split(" - ")[1]
                    tag.artist = info_dict["title"].split(" - ")[0]
                    title = info_dict["title"].split("-")[1]
                elif(len(info_dict["title"].split("-")) > 1):
                    tag.title = info_dict["title"].split("-")[1]
                    tag.artist = info_dict["title"].split("-")[0]
                    title = info_dict["title"].split("-")[1]
                else:
                    tag.title = info_dict["title"]
                    title = info_dict["title"]

                tag.save()
                os.rename(info_dict["title"]+'-' +info_dict["id"]+".mp3",settings["pathMusique"] + '/ToSort/'+ title + ".mp3")


elif(str(sys.argv[1]) == 'full'):
    tag = id3.Tag()
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
        if "https://www.youtube.com/watch?" in i:
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist:': 'true',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print(i)
                info_dict = ydl.extract_info(i.split("&index")[0].split("&list=")[0], download=False)
                ydl.download([i.split("&index")[0].split("&list=")[0]])
                tag.parse(info_dict["title"]+'-' +info_dict["id"]+".mp3")

                top = tkinter.Tk()
                done = False
                def delWindow(a):
                    done = False
                    top.quit()
                def CloseWindow():
                    done = True
                    top.quit()
                top.title("Youtube to MP3")
                title = tkinter.StringVar()
                artist = tkinter.StringVar()
                tkinter.Label(top,text=info_dict["title"]).grid(column=2, row=1)
                tkinter.Label(top,text="Titre",width=10).grid(column=1, row=2)
                tkinter.Entry(top,text="Titre",textvariable=title).grid(column=2, row=2)
                tkinter.Label(top,text="Artiste").grid(column=1, row=3)
                tkinter.Entry(top,text="Artiste",textvariable=artist).grid(column=2, row=3)
                tkinter.Label(top,text="").grid(column=2, row=4)
                top.bind("<KeyPress-Escape>",delWindow)
                tkinter.Button(top,text="Convertir",command=CloseWindow,width=10).grid(column=3,row=5)
                top.mainloop()
                if done == True:
                    tag.title = title.get()
                    tag.artist = artist.get()
                    title = title.get()

                    tag.save()
                    os.rename(info_dict["title"]+'-' +info_dict["id"]+".mp3",settings["pathMusique"] + '/ToSort/'+ title + ".mp3")
else:
    print('do it')
