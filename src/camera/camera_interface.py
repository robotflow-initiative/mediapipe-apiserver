import abc
from typing import Optional, Any
from common.option import CameraOption

class vCamera(abc.ABC):
    def __init__(self, camera_id: str, option: CameraOption) -> None:
        self.camera_id = camera_id
        self.option = option
        self.is_opened = False
        self.is_started = False
        super().__init__()
    
    @abc.abstractmethod
    def open(self) -> Optional[Exception]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def start(self) -> Optional[Exception]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def stop(self) -> Optional[Exception]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read(self) -> Any:
        raise NotImplementedError
    
    @abc.abstractmethod
    def close(self) -> Optional[Exception]:
        raise NotImplementedError