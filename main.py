import urllib.request
import random
import pafy
import vlc
from bs4 import BeautifulSoup
import time
import os



def readfile():
    f = open(os.path.dirname(os.path.abspath(__file__))+"/Songs.txt", "r")
    return f.read()

def search(textToSearch):
    return "https://www.youtube.com" + BeautifulSoup(urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(textToSearch)).read(), 'html.parser').findAll("a", attrs={"class":"yt-uix-tile-link"})[1]["href"]



artists = readfile().split("\n\n")
artists = [i.split("\n") for i in artists]
songs = [i for j in artists for i in j]
songs = [i.split(" - ") for i in songs]
while True:
    randomnum = random.randint(0, len(songs))
    cursong = songs[randomnum][0]+" "+songs[randomnum][1]
    print(cursong)
    url = search(cursong)
    video = pafy.new(url)
    sleeptime = video.length
    best = video.getbest()
    # playurl = best.url
    playurl = video.getbestaudio().url
    p = vlc.MediaPlayer(playurl)
    p.play()
    time.sleep(sleeptime)
    p.stop()
