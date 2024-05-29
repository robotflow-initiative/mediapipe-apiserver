import abc
from typing import Optional, Any
from mediapipe_apiserver.common.option import CameraOption
from mediapipe_apiserver.common.datamodels import IntrinsicsMatrix

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