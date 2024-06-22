# linux-nvr

A simple Python script to transform a Linux machine into a Network Video Recorder (NVR). The script streams video from IP cameras in your network and splits the video into pre-determined segments (by default, 10-minute-long segments). The videos are stored on your local hard drive. This tool is ideal for those who do not require fancy GUIs, motion detection, etc., and wish to build a cost-effective NVR using inexpensive cameras available online.

The script uses the RTSP protocol and calls [FFmpeg](https://ffmpeg.org/) to handle the video streams.

## Features
- Supports multiple IP cameras
- Configurable recording period
- Customizable video and audio codecs
- Organized output directory structure by date

## Usage

To record footage from a camera in 10-minute chunks:

```sh
python record.py --camera camera1 --record-period 600
```

### Command-line Arguments

- `--camera`: Name of the camera. Configure the camera's RTSP URL in the script.
- `--record-period`: Output file size in seconds. Default is 600.
- `--video-codec`: FFmpeg codec (copy or libx264). Default is libx264.
- `--video-scale`: Video scale (only for libx264). Default is 1280:-1.
- `--video-preset`: libx264 preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow). Default is veryfast.
- `--video-crf`: libx264 CRF (0-51, lower is better quality). Default is 25.
- `--video-format`: Output video format (mp4, avi, or other). Default is mp4.
- `--audio-codec`: Audio codec (copy or aac). Default is aac.
- `--audio-bitrate`: Audio bitrate (64k for mono, 128k for stereo). Default is 64k.

To see this list in the console, use

```sh
python record.py --help
```

### Example

To record from camera1 in 5-minute segments using libx264 codec:

```sh
python record.py --camera camera1 --record-period 300 --video-codec libx264 --video-scale 1280:-1 --video-preset fast --video-crf 23 --video-format mp4 --audio-codec aac --audio-bitrate 128k
```

## Camera Configuration

Edit the camera's RTSP URL in the script:

```
if args.camera == "camera1":
    cam = 'rtsp://username:password@ip:port/url'
elif args.camera == "camera2":
    cam = 'rtsp://username:password@ip:port/url'
```

You might need to modify the RTSP command in `record.py` to match your camera's format. Refer to the camera's user manual or check [this comprehensive list of RTSP commands](https://www.ispyconnect.com/sources.aspx) for many brands.

## Deleting Old Videos

Use a `cron` job to delete old videos. For example, to delete files older than 7 days:

```
find /path/to/videos -type f -mtime +7 -exec rm {} \;
```

Add the above command to your `crontab` to automate the deletion process. You can find more details on setting up `cron` jobs [here](https://askubuntu.com/questions/789602/auto-delete-files-older-than-7-days).

## Prerequisites

1. Install FFmpeg:

```
sudo apt install ffmpeg
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss changes or improvements.

## Support

If you encounter any issues or have any questions, please open an issue on GitHub.

---

*Please ensure that the IP address and RTSP path for your camera are correctly configured in the script before running it.*
