from mediapipe_apiserver.common.option import CameraOption
from typing import Any, Optional

import cv2
import numpy as np
import os
import time
from .camera_interface import vCamera

class FileCamera(vCamera):
    def __init__(self, camera_loc: str, option: CameraOption) -> None:
        super().__init__(camera_loc, option)
        self.media_files = []
        self.current_media_index = 0
        self.video_capture = None
        self.is_video_file = False
        self.timestamp = None
        if os.path.isdir(camera_loc):
            # camera_loc is a directory containing image and video files
            all_files = sorted([
                os.path.join(camera_loc, f) for f in os.listdir(camera_loc)
                if os.path.isfile(os.path.join(camera_loc, f))
            ])
            # Filter out image and video files
            self.media_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.mp4', '.avi', '.mov'))]
            if not self.media_files:
                raise Exception("No valid media files found in the specified directory.")
        else:
            raise Exception("camera_id must be a directory containing media files.")

    def open(self) -> Optional[Exception]:
        
        self.is_opened = True
        self.is_started = True  # First open will automatically start the 'camera'
        self.current_media_index = 0  # Reset to the first file

    def start(self) -> Optional[Exception]:
        if not self.is_opened:
            return Exception("not opened")
        if self.is_started:
            return Exception("already started")
        self.is_started = True

    def read(self) -> Any: #每次read读取一帧或者一张图片
        #检查错误
        if not self.is_started:
            return None, Exception("not started")
        if self.current_media_index >= len(self.media_files):
            return None, Exception("No more files")
        self.timestamp = time.time() 
        current_file = self.media_files[self.current_media_index]
        if current_file.lower().endswith(('.mp4', '.avi', '.mov')):
            if not self.video_capture:
                self.video_capture = cv2.VideoCapture(current_file)
                self.is_video_file = True
            ret, frame = self.video_capture.read()
            if not ret:
                self.video_capture.release()
                self.video_capture = None
                self.is_video_file = False
                self.current_media_index += 1  # Move to the next media file
                return self.read()  # Recursively read the next media file
            return frame, None
        else:
            if self.is_video_file and self.video_capture:
                self.video_capture.release()
                self.video_capture = None
                self.is_video_file = False
            image = cv2.imread(current_file)
            if image is None:
                return None, Exception(f"Failed to read image from {current_file}")
            self.current_media_index += 1
            return image, None

    def stop(self) -> Optional[Exception]:
        if not self.is_started:
            return Exception("already stopped.")
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.is_started = False

    def close(self) -> Optional[Exception]:
        if not self.is_opened:
            return Exception("already closed")
        if self.is_started:
            return Exception("not stopped")
        self.is_opened = False
        self.current_media_index = 0  # 重置相机
        
