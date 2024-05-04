from src.common.option import CameraOption
from typing import Any, Optional

import cv2
import numpy as np
import pykinect_azure as pykinect

from .camera_interface import vCamera

_library_initialized = False

class KinectCamera(vCamera):
    def __init__(self, camera_id: str, option: CameraOption) -> None:
        super().__init__(camera_id, option)
        global _library_initialized
        if not _library_initialized:
            pykinect.initialize_libraries()
            _library_initialized = True
        if camera_id is None or camera_id == "":
            self._camera_index = 0
        else:
            try:
                self._camera_index = int(camera_id)
            except ValueError:
                raise Exception("camera_id(index) must be a integer")
        assert self._camera_index >= 0, "camera_id(index) must be a positive integer"
        
        self._device: pykinect.Device = None
        self._device_config: pykinect.Configuration = None

    def open(self) -> Optional[Exception]:
        _device_config = pykinect.default_configuration
        if self.option.use_depth:
            _device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
            _device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        else:
            _device_config.depth_mode = pykinect.K4A_DEPTH_MODE_OFF
            _device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P

        self._device = pykinect.start_device(device_index=self._camera_index, config=_device_config)
        self._device_config = _device_config
        self.is_opened = True
        self.is_started = True
        return None

    def start(self) -> Optional[Exception]:
        if not self.is_opened:
            return Exception("not opened")
        if self.is_started:
            return Exception("already started")
        self._device.start_cameras(self._device_config)
        self.is_started = True

    def read(self) -> Any:
        if not self.is_started:
            return Exception("not started")
         # Get capture
        capture = self._device.update()

        # Get the color depth image from the capture
        if self.option.use_depth:
            ret, image = capture.get_depth_image()
            image = cv2.convertScaleAbs(image, alpha=0.05)
            image = np.stack((image,)*3, axis=-1)  ## input should be 3 channel
        else:
            ret, image = capture.get_color_image()

        return image, None if ret else Exception("empty frame")

    def stop(self) -> Optional[Exception]:
        if not self.is_started:
            return Exception("already stopped")
        self._device.stop_cameras()
        self.is_started = False
        return None

    def close(self) -> Optional[Exception]:
        if self.is_closed:
            return Exception("already closed")
        if self.is_started:
            return Exception("not stopped")
        self._device.close()
        self.is_opened = False
        self._device = None
        self._device_config = None

