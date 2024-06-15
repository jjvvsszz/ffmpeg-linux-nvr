'''
Simple recorder for cheap IP cameras using ffmpeg
Usage:
    Record camera1's footage in 600 second chunks
    python record.py --camera camera1 --record-period 600
    
'''

import subprocess
import time
import os
import signal
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--camera", type=str, default="camera1",
                    help="Camera (camera1 or camera2)")
parser.add_argument("--record-period", type=int, default=600,
                    help="Output file size in seconds")
args = parser.parse_args()

common =' -vf scale=1280:-1 -c:v libx264 -preset superfast -crf 25 -c:a aac -b:a 128k'

if args.camera == "camera1":
    # modify the IP address below to your camera1's IP
    # RTSP path might be different for each camera brand
    # also, modify the username and password
    # default might be like "admin:admin" or "admin:"
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
    fl = time.ctime().replace(' ', '_')
    fl = fl.replace(':', '_')
    return fl

while True:
    start_time = time.time()

    filename = return_filename()
    outfile = './%s/%s.mp4' % (outdir, filename)
    # Create the ffmpeg command and its parameters
    cmd = f'ffmpeg -rtsp_transport tcp -i ' + cam + common  + ' ' + outfile
    cmd = cmd.split(' ')
    cmd = [ix for ix in cmd if ix != '']

    subprocess.run(cmd)

    elapsed = time.time() - start_time
    print('Elapsed %1.2f' % (elapsed))
