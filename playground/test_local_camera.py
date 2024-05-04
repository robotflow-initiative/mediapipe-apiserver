import cv2
import pykinect_azure as pykinect
import numpy as np

from src.camera import KinectCamera 
from src.detector import MediaPipeDetector
from src.common.option import CameraOption
is_depth = False

from loguru import logger

def main():
    opt = CameraOption(use_depth=False)
    cam = KinectCamera("0")
    detector = MediaPipeDetector()

    cam.open()
    cam.start()

    cv2.namedWindow('Annoed Depth Image',cv2.WINDOW_NORMAL)
    try:
        while True:
            # Get capture
            image, err = cam.read()
            if err is not None:
                logger.error(err)
                break
            annoed, uvs = detector.get_landmarks(image)
            cv2.imshow('Annoed Depth Image', annoed)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'):  
                break
    except KeyboardInterrupt:
        print("Keyboard Interrupt Captured")
    finally:
        cv2.destroyAllWindows()
