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
import sqlite3


PATH_TO_SONGS = "~/home/$USER/Desktop/"

conn = sqlite3.connect(PATH_TO_SONGS+'songs.db')
c = conn.cursor()


def search(textToSearch, id=0):
    return "https://www.youtube.com" + BeautifulSoup(urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(textToSearch)).read(), 'html.parser').findAll("a", attrs={"class": "yt-uix-tile-link"})[id]["href"]


class Song:
    def __init__(self, title, artist, id=0):
        self.title = title
        self.artist = artist
        self.id = id
        while True:
            try:
                if len(search(title+" - "+artist, self.id)) > 44:
                    self.id += 1
                else:
                    self.url = search(title+" - "+artist, self.id)
                    break
            except:
                self.id += 1

    def play(self, video=False):
        audio = pafy.new(self.url)
        sleeptime = audio.length
        if video:
            playurl = audio.getbest().url
        else:
            playurl = audio.getbestaudio().url
        self.p = vlc.MediaPlayer(playurl)
        p.play()

    def stop(self):
        self.p.stop()


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


args = getArgs()
if args.Song = None:
