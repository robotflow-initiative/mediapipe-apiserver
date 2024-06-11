import abc
from typing import Optional, Any
from mediapipe_apiserver.common.option import CameraOption
from mediapipe_apiserver.common.datamodels import IntrinsicsMatrix

import threading
import queue


class vCamera(abc.ABC):
    """This is abstract camera interface"""

    def __init__(self, camera_id: str, option: CameraOption) -> None:
        self.camera_id = camera_id
        self.option = option
        self.is_opened = False
        self.is_started = False
        super().__init__()

    @abc.abstractmethod
    def open(self) -> Optional[Exception]:
        """open the camera, but do not start"""
        raise NotImplementedError

    @abc.abstractmethod
    def start(self) -> Optional[Exception]:
        """start the camera"""
        raise NotImplementedError

    @abc.abstractmethod
    def read(self) -> Any:
        """read from an opened camera"""
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self) -> Optional[Exception]:
        """stop the camera"""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> Optional[Exception]:
        """close a stopped camera"""
        raise NotImplementedError

    @abc.abstractmethod
    def device(self) -> Optional[Any]:
        """return the raw device"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_intrinsics(self) -> Optional[IntrinsicsMatrix]:
        """return the intrinsics"""
        raise NotImplementedError


class AsyncCamera(vCamera):
    
    def __init__(self, base_camera: vCamera) -> None:
        def _producer(camera, queue):
            while camera.is_started:
                frame, err = camera.read()
                if err is not None:
                    raise err
                queue.put(frame)

        self.base_camera = base_camera
        self.frame_queue = queue.LifoQueue(maxsize=10)
        self.worker = threading.Thread(target=_producer, args=(self.base_camera, self.frame_queue))

    def open(self) -> Optional[Exception]:
        return self.base_camera.open()
    
    def start(self) -> Exception | None:
        rtn = self.base_camera.start()
        self.worker.start()
        return rtn

    def read(self) -> Any:
        frame = self.frame_queue.get()
        self.frame_queue.task_done()
        return frame, None
    
    def stop(self) -> Exception | None:
        rtn = self.base_camera.stop()
        while not self.frame_queue.empty():
            self.frame_queue.get()
            self.frame_queue.task_done()
        return rtn
    
    def close(self) -> Exception | None:
        rtn = self.base_camera.close()
        while not self.frame_queue.empty():
            self.frame_queue.get()
            self.frame_queue.task_done()
        return rtn
    
    def device(self) -> Any:
        return self.base_camera.device()
    
    def get_intrinsics(self) -> Optional[IntrinsicsMatrix]:
        return self.base_camera.get_intrinsics()
