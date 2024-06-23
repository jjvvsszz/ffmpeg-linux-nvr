import subprocess
import time
from datetime import datetime
from pathlib import Path
import os
import signal
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--camera", type=str, default="camera1",
                    help="Name of the camera. Configure in script")
parser.add_argument("--record-period", type=int, default=600,
                    help="Output file size in seconds. Default is 600")
parser.add_argument("--video-codec", type=str, default="libx264",
                    help="FFmpeg codec (copy or libx264). Default is libx264")
parser.add_argument("--video-scale", type=str, default="1280:-1",
                    help="Video scale (only in libx264). Default is 1280:-1")
parser.add_argument("--video-preset", type=str, default="veryfast",
                    help="libx264 preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow). Default is vertfast")
parser.add_argument("--video-crf", type=str, default="25",
                    help="libx264 crf (0-51, lower is better quality). Default is 25")
parser.add_argument("--video-format", type=str, default="mp4",
                    help="FFmpeg codec (mp4, avi or other). Default is mp4")
parser.add_argument("--audio-codec", type=str, default="aac",
                    help="FFmpeg codec (copy or aac). Default is aac")
parser.add_argument("--audio-bitrate", type=str, default="64k",
                    help="64k if mono and 128k if stereo. Default is 64k")
args = parser.parse_args()

if args.video_codec == "copy":
    videoargs  = '-c:v copy'
elif args.video_codec == "libx264":
    videoargs = '-fflags +genpts -err_detect ignore_err -vf scale=%s -c:v libx264 -preset %s -crf %s -movflags +faststart -async 1 -vsync 1' % (args.video_scale, args.video_preset, args.video_crf)

if args.audio_codec == "copy":
    audioargs  = '-c:a copy'
elif args.audio_codec == "aac":
    audioargs = '-c:a aac -b:a %s' % args.audio_bitrate

common =' %s %s' % (videoargs, audioargs)

if args.camera == "camera1":
    # modify the IP address below to your camera1's IP
    # RTSP path might be different for each camera brand
    # also, modify the username and password
    # default might be like admin:admin 
    cam = 'rtsp://username:password@ip:port/url'
elif args.camera == "camera2":
    cam = 'rtsp://username:password@ip:port/url'

common = common + ' -t %d ' % args.record_period
# Create the output directory
outdir = './%s/' % args.camera
os.system('mkdir -p %s' % outdir)

def return_filename():
    # Creates a filename with the start time
    # of recording in its name
    fl = datetime.now()
    Path(fl.strftime(outdir + "%Y/%m/%d")).mkdir(parents=True, exist_ok=True)
    fl = fl.strftime("%Y/%m/%d/%H-%M-%S")
    return fl

while True:
    start_time = time.time()

    filename = return_filename()
    outfile = './%s/%s.%s' % (outdir, filename, args.video_format)
    # Create the ffmpeg command and its parameters
    cmd = f'ffmpeg -rtsp_transport tcp -timeout 5000000 -rw_timeout 10000000 -i ' + cam + common  + ' ' + outfile
    cmd = cmd.split(' ')
    cmd = [ix for ix in cmd if ix != '']

    try:
        subprocess.run(cmd, timeout=args.record_period+1)
    except subprocess.TimeoutExpired:
        print(f"O processo foi encerrado após {args.record_period + 1} segundos.")

    elapsed = time.time() - start_time
    print('Elapsed %1.2f' % (elapsed))

