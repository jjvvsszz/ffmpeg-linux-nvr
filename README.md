# linux-nvr
This is a simple python script to use a Linux machine as an NVR. The code streams video from IP cameras in your network and splits the video into pre-determined segments (by default, 10 minute-long segments). The videos are stored in your local hard-drive. If you do not need any fancy GUIs, motion detection, etc., this is a simple tool to build your own NVR with cheap cameras purchased online. 

This is achieved using RTSP protocol, and the code calls [FFmpeg](https://ffmpeg.org/). See prerequisites for FFmpeg installation instructions.

## Usage:
`python record.py --camera camera1 --record-period 600`

*Please edit camera1's IP address in the code. Also, you might need to modify the RTSP command in `record.py` to match your camera's format. You can find that format from the camera's user manual. [This](https://www.ispyconnect.com/sources.aspx) webpage also has a comprehensive list of RTSP commands for many brands.*

## Deleting old videos
I use a `cron` job to delete old videos. You can find an example [here](https://askubuntu.com/questions/789602/auto-delete-files-older-than-7-days).

## Motivation
In theory, openRTSP should automatically perform streaming the video and splitting it into pre-determined chunks. In practice, I found out that RTSP connections drop and saved files are much longer than they should be, with frequent errors. The goal of this script is to run openRTSP only for relatively short periods of time (10 minutes each), and open a new stream every 10 minutes.

## Prerequisites
* Install FFmpeg:
`sudo apt install ffmpeg`
