# SongShuffle
Place your favourite songs in Songs.txt and it will automatically find it on youtube and play a random song.
## Disclaimer
**Still in BETA**<br/>
**NO ANIMALS WERE HURT DURING THE PROGRAMMING**<br/>
**I'm NOT responsible for any damage**
## Requirements
_**[Python 3.X.X](https://www.python.org/downloads/release/python-372/)**_ (Tested on [Python3.6.6](https://www.python.org/downloads/release/python-366/))<br />
_**[VLC Player](https://www.videolan.org/vlc/download-windows.html)**_
## Installation
### Basic
```
pip3 install pafy
pip3 install youtube-dl
pip3 install beautifulsoup4
pip3 install python-vlc
```
### Adding Songs
Edit `Songs.txt` file.<br/>
Formating rules are:
- Every song must have **artist specified**
- Songs and artists must be separeted by **" - "**
- Different artist must be separated by **double "\n"**<br/>

You can see how my songs are **formated**.
### Optional
Adding it to path is awesome!

## Usage
`--song` or `-s` for searching a song (default: search on youtube)<br />
`--listed` or `-l` for searching in `Songs.txt`<br />
`--noautoplay` or `-a` to play just once<br />
`--help` or `-h` for usage
## Changelog
- Added Argparser for CLI
- Fixed errors
- Updated README
## Credits
Created by [Alexa Ognjanovic](https://www.github.com/proalexa/)
