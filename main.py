import urllib.request
import random
import pafy
import vlc
from bs4 import BeautifulSoup
import time
import os
import sys


def readfile():
    f = open(os.path.dirname(os.path.abspath(__file__))+"/Songs.txt", "r")
    return f.read()


def search(textToSearch):
    return "https://www.youtube.com" + BeautifulSoup(urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(textToSearch)).read(), 'html.parser').findAll("a", attrs={"class": "yt-uix-tile-link"})[0]["href"]


def play(url):
    video = pafy.new(url)
    sleeptime = video.length
    playurl = video.getbestaudio().url
    p = vlc.MediaPlayer(playurl)
    p.play()
    time.sleep(sleeptime)
    p.stop()


artists = readfile().split("\n\n")
artists = [i.split("\n") for i in artists]
songs = [i for j in artists for i in j]
songs = [i.split(" - ") for i in songs]

if len(sys.argv) == 2:
    # inSongs = False
    # for i, j in enumerate(songs):
    #     if sys.argv[1].lower() in j[0].lower():
    #         res = search(songs[i][0] + " " + songs[i][1])
    #         inSongs = True
    # if inSongs == False:
    #     res = search(" ".join(sys.argv[1]))
    # print(res)
    # play(res)
    # Doesn't work well :)
    play(search(sys.argv[1]))

def main():
    try:
        while True:
            randomnum = random.randint(0, len(songs))
            cursong = songs[randomnum][0] + " " + songs[randomnum][1]
            url = search(cursong)
            play(url)
    except:
        main()
main()