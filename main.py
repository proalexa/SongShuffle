#!/usr/bin/python3
import urllib.request
import random
import pafy
import vlc
from bs4 import BeautifulSoup
import time
import os
import sys
import argparse


def readfile():
    f = open(os.path.dirname(os.path.abspath(__file__))+"/Songs.txt", "r")
    return f.read()


songs = [i.split(" - ") for i in [i for j in [i.split("\n")
                                              for i in readfile().split("\n\n")] for i in j]]


def getArgs():
    parser = argparse.ArgumentParser(
        description='Play songs from youtube from CLI!')
    parser.add_argument("--song", '-s', type=str,
                        help='Search songs online.', default=None, metavar="Song")
    parser.add_argument("--id", '-i', type=int,
                        help='Id of song foung on youtube', default=0, metavar="id")
    parser.add_argument("--listed", '-l', help='Search songs in Songs.txt file.',
                        default=False, action='store_const', const=True)
    parser.add_argument("--noautoplay", "-a", help='Add to end after song.',
                        default=True, dest='autoplay', action='store_const', const=False)
    parser.add_argument("--add", type=str, metavar="add",
                        help="Add song to database", default=None)
    parser.add_argument("--remove", type=str, metavar="remove",
                        help="Remove song from database", default=None)
    args = parser.parse_args()
    return args


def search(textToSearch, id=0):
    return "https://www.youtube.com" + BeautifulSoup(urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(textToSearch)).read(), 'html.parser').findAll("a", attrs={"class": "yt-uix-tile-link"})[id]["href"]


def play(url):
    video = pafy.new(url)
    sleeptime = video.length
    playurl = video.getbestaudio().url
    p = vlc.MediaPlayer(playurl)
    p.play()
    time.sleep(sleeptime)
    p.stop()


args = getArgs()
r = random.choice(songs)
songUrl = search(r[0]+" - "+r[1], args.id)

if not args.song == None:
    if args.listed == True:
        for i in songs:
            if args.song.lower() in i[0].lower():
                songUrl = search(i[0]+' '+i[1], args.id)
    else:
        songUrl = search(args.song, args.id)

while True:
    play(songUrl)
    if args.autoplay == False:
        break
    r = random.choice(songs)
    songUrl = search(r[0]+" - "+r[1], args.id)
