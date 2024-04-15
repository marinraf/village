import os
import time
from pprint import pprint

import cv2
from libcamera import controls
from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput

from village.fake import Fake
from village.log import log
from village.settings import settings

# info about picamera2: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf


# configure the logging of libcamera (the C++ library picamera2 uses)
os.environ["LIBCAMERA_LOG_LEVELS"] = "2"
#'0' = DEBUG, '1' = INFO, '2' = WARNING, '3' = ERROR, '4' = FATAL


# use this function to get info
def print_info_about_the_connected_cameras():
    print("INFO ABOUT THE CONNECTED CAMERAS:")
    pprint(Picamera2.global_camera_info())
    print("")


# the camera class
class Camera:
    """
    Camera class to handle the camera and the video recording.
    The camera is a Picamera2 object.
    """

    def __init__(self, index, name):
        cam_raw = {"size": (2304, 1296)}
        cam_main = {"size": (640, 480)}
        cam_controls = {
            "FrameDurationLimits": (33333, 33333),
            "AfMode": controls.AfModeEnum.Manual,
            "LensPosition": 0.0,
        }
        encoder_quality = Quality.VERY_LOW
        # VERY_LOW, LOW, MEDIUM, HIGH, VERY_HIGH

        self.index = index
        self.name = name
        self.encoder_quality = encoder_quality
        self.encoder = H264Encoder()
        self.cam = Picamera2(index)
        self.config = self.cam.create_video_configuration(
            raw=cam_raw, main=cam_main, controls=cam_controls
        )
        self.cam.align_configuration(self.config)
        self.cam.configure(self.config)
        self.path_video = os.path.join(
            settings.get("DATA_DIRECTORY"), "videos", name + ".mp4"
        )
        self.output = FfmpegOutput(self.path_video)
        self.cam.pre_callback = self.apply_timestamp

        self.cam.start()

    def start_camera(self):
        self.cam.start()

    def stop_preview(self):
        self.cam.stop_preview()

    def reset_preview(self):
        self.cam.start_preview(Preview.NULL)

    def start_record(self):
        self.cam.start_encoder(self.encoder, self.output, quality=self.encoder_quality)

    def stop_record(self):
        self.cam.stop_encoder()

    def stop(self):
        self.cam.stop()

    def change_focus(self, lensposition):
        assert isinstance(
            lensposition, (int, float)
        ), "lensposition must be int or float"
        assert (
            lensposition <= 10 and lensposition >= 0
        ), "lensposition must be a value between 0 and 10"
        self.cam.set_controls({"LensPosition": lensposition})

    def change_framerate(self, framerate):
        assert isinstance(framerate, int), "framerate must be int"
        limit = int(1000000.0 / float(framerate))
        # limit is the min and max number of microseconds for each frame
        self.cam.set_controls({"FrameDurationLimits": (limit, limit)})

    def print_info_about_config(self):
        print("INFO ABOUT THE " + self.name + " CAM CONFIGURATION:")
        pprint(self.config)
        print("")

    def apply_timestamp(self, request):
        colour = (0, 255, 0)
        origin1 = (0, 30)
        origin2 = (0, 60)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1
        thickness = 2
        threshold = 50
        timestamp = time.strftime("%Y-%m-%d %X")
        with MappedArray(request, "main") as m:
            greyscale_frame = cv2.cvtColor(m.array, cv2.COLOR_BGR2GRAY)
            gaussian_frame = cv2.GaussianBlur(greyscale_frame, (5, 5), 0)
            t = cv2.threshold(gaussian_frame, threshold, 225, cv2.THRESH_BINARY_INV)[1]
            area = cv2.countNonZero(t)
            cv2.putText(m.array, timestamp, origin1, font, scale, colour, thickness)
            cv2.putText(m.array, str(area), origin2, font, scale, colour, thickness)


try:
    cam_corridor = Camera(0, "CORRIDOR")
    cam_box = Camera(1, "BOX")
    cam_corridor.start_record()
    cam_box.start_record()
    log("successfully imported cam_box and cam_corridor")
except Exception as e:
    log("Could not create camera: ", exception=e)
    cam_box = Fake()
    cam_corridor = Fake()
