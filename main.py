#!/usr/bin/python
import urllib.request
import random
import pafy
import vlc
from bs4 import BeautifulSoup
from time import sleep
import os
import sys
import argparse
import sqlite3
from prettytable import PrettyTable
from tqdm import tqdm


class SQLController:
    def __init__(self, filename):
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

    def add(self, title, artist):
        self.cursor.execute(
            "INSERT INTO Songs (title,artist) VALUES (?,?);", (title, artist))
        self.connection.commit()

    def remove(self, iid):
        self.cursor.execute("DELETE FROM Songs WHERE ID=?;", (iid,))
        self.connection.commit()

    def fetchSongs(self):
        return [Song(i[1], i[2], sid=i[3]) for i in self.cursor.execute("SELECT * FROM Songs;")]

    def updateSid(self, iid, sid):
        self.cursor.execute("UPDATE Songs SET sid=? WHERE ID=?", (sid, iid))
        self.connection.commit()


class Song:
    def __init__(self, title, artist, sid=0):
        self.title = title
        self.artist = artist
        self.sid = sid

    def sync(self):
        while True:
            searched = search(self.title+" - "+self.artist, self.sid)
            if len(searched) > 44:
                self.sid += 1
            else:
                self.url = searched
                break
        return self.sid

    def play(self, video=False):
        self.url = search(self.title+" - "+self.artist, self.sid)
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
    parser.add_argument("--echo", '-e', help='Print all listed Songs.',
                        default=False, action='store_const', const=True)
    parser.add_argument("--add", type=str, metavar="add",
                        help="Add song to database", default=None)
    parser.add_argument("--remove", type=int, metavar="remove",
                        help="Remove song from database", default=None)
    parser.add_argument("--ignoredb", '-i', help='Don\'t create songs.db Just playsongs without it.',
                        default=False, action='store_const', const=True)
    # Instead of this I will implement searchby argument
    parser.add_argument("--byid", '-b', help='Play song by songdb id',
                        default=False, action='store_const', const=True)
    parser.add_argument("--play", "-p", type=str, metavar="play",
                        help="Playsongs", default=None)
    parser.add_argument("--shuffle", '-8', help='Shuffle Songs in SQLite3 database.',
                        default=False, action='store_const', const=True)
    parser.add_argument("--video", '-v', help='Show music Video.',
                        default=False, action='store_const', const=True)
    args = parser.parse_args()
    return args


args = getArgs()
if not args.ignoredb:
    sqlc = SQLController(
        '/'.join(os.path.realpath(__file__).split("/")[:-1])+"/songs.db")
    songlist = sqlc.fetchSongs()
    if args.shuffle:
        while True:
            songToPlay = random.choice(songlist)
            songToPlay.play(video=args.video)
            sleep(songToPlay.sleeptime)
            songToPlay.stop()
    if args.echo:
        t = PrettyTable()
        t.field_names = ["ID", "Title", "Artist", "SID"]
        for i, j in enumerate(songlist):
            t.add_row([i, j.title, j.artist, j.sid])
        print(t)
    if args.add:
        songtitle = ' '.join(args.add.split("-")[0].split("."))
        songartist = ' '.join(args.add.split("-")[1].split("."))
        sqlc.add(songtitle, songartist)
    if args.remove:
        print("Do you want to remove this song:" +
              songlist[args.remove].title+" by "+songlist[args.remove].artist+"?[Y/n]")
        an = input()
        if an == "Y" or an == "" or an == "y":
            print(songlist[args.remove].title+" removed.")

    if args.sync:
        with tqdm(total=len(songlist)) as probar:
            for i, j in enumerate(songlist):
                sqlc.updateSid(i+1, j.sync())
                probar.update(1)
else:
    if not args.play:
        print("Nothing to do! exiting!")
        exit()
if args.play:
    if args.byid:
        songtitle = songlist[int(args.play)].title
        songartist = songlist[int(args.play)].artist
    else:
        songtitle = ' '.join(args.play.split("-")[0].split("."))
        songartist = ' '.join(args.play.split("-")[1].split("."))
    songToPlay = Song(songtitle, songartist)
    songToPlay.play(video=args.video)
    sleep(songToPlay.sleeptime)
    songToPlay.stop()
