from mediapipe_apiserver.common.option import CameraOption
from mediapipe_apiserver.common.datamodels import IntrinsicsMatrix
from typing import Any, Optional

import cv2
import numpy as np

from .camera_interface import vCamera


class ZED2Camera(vCamera):
    def __init__(self, camera_id: str, option: CameraOption) -> None:
        super().__init__(camera_id, option)

        self.cam = None

    def open(self)  -> Optional[Exception]:
        self.cam = cv2.VideoCapture(int(self.camera_id))
        self.cam.set(cv2.CAP_PROP_FPS, 60)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.is_opened = True
        self.is_started = True

    def start(self) -> Optional[Exception]:
        # avoid duplicate start
        if not self.is_opened:
            return Exception("not opened")
        if self.is_started:
            return Exception("already started")
        self.is_started = True

    def read(self) -> Any:
        # avoid reading from stopped camera
        if not self.is_started:
            return Exception("not started")

        # get capture
        ret, frame = self.cam.read()
        
        # select the left half
        frame = frame[:, :1280]

        return frame, None if ret else Exception("empty frame")

    def stop(self) -> Optional[Exception]:
        # avoid stop a stopped camera
        if not self.is_started:
            return Exception("already stopped")
        self.is_started = False
    
    def close(self) -> Optional[Exception]:
        # avoid close a closed camera or started camera
        if not self.is_opened:
            return Exception("already closed")
        if self.is_started:
            return Exception("not stopped")
        self.cam.release()
        self.is_opened = False

        # reset properties
        self.cam = None

    @property
    def device(self):
        return self.cam
    
    def get_intrinsics(self) -> Optional[IntrinsicsMatrix]:
        raise NotImplementedError
