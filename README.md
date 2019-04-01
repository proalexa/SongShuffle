# SongShuffle
Place your favourite songs in Songs.txt and it will automatically find it on youtube and play a random song.
## Disclaimer
**Documentation is DEPRECATED, Updating soon!**
## Requirements
_**[Python 3.X.X](https://www.python.org/downloads/release/python-372/)**_ (Tested on [Python3.6.6](https://www.python.org/downloads/release/python-366/) and [Python3.7.0](https://www.python.org/downloads/release/python-370/))<br />
_**[VLC Player](https://www.videolan.org/vlc/download-windows.html)**_
## Installation
### Basic
```
pip3 install pafy
pip3 install youtube-dl
pip3 install beautifulsoup4
pip3 install python-vlc
```
or
```
pip3 install -r requirements.txt
```
### Adding Songs DEPRECATED
Edit `Songs.txt` file.<br/>
Formating rules are:
- Every song must have **artist specified**
- Songs and artists must be separeted by **" - "**
- Different artist must be separated by **double "\n"**<br/>

You can see how my songs are **formated**.
### Optional
Adding it to path is awesome!

## Usage DEPRECATED
`--song` or `-s` for searching a song (default: search on youtube)<br />
`--listed` or `-l` for searching in `Songs.txt`<br />
`--noautoplay` or `-a` to play just once<br />
`--help` or `-h` for usage
## TODO
- Replace VLC with PyGame for portability
- Integrate YouTube autoplay feature
- Update README
## Changelog
- Added Argparser for CLI
- Added Shuffle
- Added SQLite3
- Song list is not necessary
- Fixed errors
- Updated README
## Known Issues
- Sometimes error 403: Access Denied of URL
- Sometimes length of video is shortened.
## Credits
Created by [Alexa Ognjanovic](https://www.github.com/proalexa/)
