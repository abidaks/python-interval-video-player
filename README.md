# Python Interval Video Player using OpenCV and PyAudio

This repository contains simple code written in python to create a basic video player using OpenCV and PyAudio.
It is a simple project using multiprocessing and shared moemory to run both audio and video simultanioulsy.

## Features of this Player

* You can pause video by pressing "space" button from keyboard
* You can stop video by pressing "s" button from keyborad
* The video pause itself on specific time intervals then you need to press space button to play again
* More features to come

## Installing this module

### Local installation

> **Requirements**
>
> This project has been tested in Ubuntu 18.04 with Python 3.6.5. Further package requirements are described in the
> `requirements.txt` file.

```
> git clone https://github.com/abidaks/python-interval-video-player
> cd python-interval-video-player
```


## Installing dependencies

run below command to install dependencies
```

> pip install requirements.txt
```

## Running Player

You need two files to run an audio file and video file.
```
python player.py --video=test.mp4 --audio=test.wav
```

You can generate audio from video file using below command
```
python splitter.py --video=test.mp4 --audio=test.wav
```

## What can be developed using this code?
Although this code can be used in so many projects here are few examples
You can make a simple speech verification program using google speech services to verify what needs to be said on specific timeframe.
You can also verify persons and poses of persons on specific time frames using facial recognition and pose detection


## License

* [GNU General Public License](http://www.gnu.org/licenses/)
