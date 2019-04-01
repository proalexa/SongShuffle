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


class SQLController:
    def __init__(self,filename):
        self.filename = filename
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        sqlCreate = """ CREATE TABLE IF NOT EXISTS Songs (
                                        ID integer PRIMARY KEY AUTOINCREMENT,
                                        title varchar(100) NOT NULL,
                                        artist varchar(100),
                                        sid int DEFAULT 0
                                    );"""
        self.cursor.execute(sqlCreate)
    def add(self,title,artist):
        self.cursor.execute("INSERT INTO Songs (title,artist) VALUES (?,?);",(title,artist))
        self.connection.commit()
    def remove(self,iid):
        removedSong = self.cursor.execute("SELECT * FROM Songs WHERE ID=?;",iid)
        self.cursor.execute("DELETE FROM Songs WHERE ID=?;",iid)
        self.connection.commit()
        return removedSong
    def fetchSongs(self):
        return [Song(i[1],i[2],sid=i[3]) for i in self.cursor.execute("SELECT * FROM Songs;")]
            


class Song:
    def __init__(self, title, artist, sid=0):
        self.title = title
        self.artist = artist
        self.sid = sid

    def findBestId(self):
        while True:
            if len(search(self.title+" - "+self.artist, self.sid)) > 44:
                self.sid += 1
                print("next sid:{}".format(self.sid))
            else:
                self.url = search(self.title+" - "+self.artist, self.sid)
                break
        return True

    def play(self, video=False):
        audio = pafy.new(self.url)
        self.sleeptime = audio.length
        if video:
            playurl = audio.getbest().url
        else:
            playurl = audio.getbestaudio().url
        self.p = vlc.MediaPlayer(playurl)
        self.p.play()

    def stop(self):
        self.p.stop()


def search(textToSearch, iid=0):
    return "https://www.youtube.com" + BeautifulSoup(urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(textToSearch)).read(), 'html.parser').findAll("a", attrs={"class": "yt-uix-tile-link"})[iid]["href"]


def getArgs():
    parser = argparse.ArgumentParser(
        description='Play songs from youtube from CLI!')
    parser.add_argument("--sync", '-s', help='Find Best SID for songs on youtube.',
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
sqlc = SQLController("./songs.db")
if args.add:
    songtitle = ' '.join(args.add.split("-")[0].split("."))
    songartist = ' '.join(args.add.split("-")[1].split("."))
    sqlc.add(songtitle, songartist)
if args.remove:
    print(sqlc.remove(args.remove))

if args.sync:
    songlist = sqlc.fetchSongs()


[print(sid, i.title, i.artist) for sid, i in enumerate(sqlc.fetchSongs())]
